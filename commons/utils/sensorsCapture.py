# -*- coding: utf-8 -*-
# @File : sensorsCapture.py
# 方案B：通过 mitmproxy 代理捕获 VoiceWave 发往神策的上报请求，实现埋点验证
# 依赖：pip install mitmproxy  （并需信任 mitmproxy CA 证书，本类自动安装到当前用户根证书）

import os
import sys
import json
import time
import socket
import shutil
import subprocess
import winreg
from pathlib import Path
from urllib.parse import urlparse

from commons.utils.readconfig import INIConfigReader
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger

logger = get_logger()

_INET_KEY = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"


class SensorsCapture:
    """
    神策埋点抓包管理器（方案B）

    用法：
        cap = SensorsCapture()
        cap.start()                 # 启动 mitmdump + 系统代理 + CA 信任
        cap.clear()                 # 触发埋点前清空已捕获事件
        # ... UI 操作触发埋点 ...
        cap.assert_event_reported("vw_login_click")   # 断言事件已上报
        cap.stop()                  # 还原代理 + 关闭 mitmdump

    也可作为上下文管理器：with SensorsCapture() as cap: ...
    """

    def __init__(self, proxy_port=8080):
        cfg = INIConfigReader()
        self.url = cfg.getconfig("sensors", "url")
        self.host = urlparse(self.url).hostname or "sensorsjourney.com"
        self.host_filter = self.host
        self.proxy_port = proxy_port
        self.events_file = str(Path(GetPath().getProjectRoot()) / "sensors_capture_events.jsonl")
        self._proc = None
        self._saved_proxy = None  # (enable, server)

    # ---------- 生命周期 ----------

    def start(self):
        """启动 mitmdump、安装 CA、开启系统代理"""
        mitmdump = self._find_mitmdump()
        if not mitmdump:
            raise RuntimeError("未找到 mitmdump，请先执行: pip install mitmproxy")

        addon = Path(__file__).parent / "sensors_addon.py"
        os.environ["SENSORS_EVENTS_FILE"] = self.events_file
        os.environ["SENSORS_HOST_FILTER"] = self.host_filter
        self.clear()

        mitmdump = self._find_mitmdump()
        cmd = [
            mitmdump,
            "-s", str(addon),
            "--listen-port", str(self.proxy_port),
            "-q",
        ]
        logger.info(f"启动 mitmdump: {' '.join(cmd)}")
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        if not self._wait_port_ready(timeout=20):
            err = self._proc.stderr.read().decode("utf-8", "ignore") if self._proc.stderr else ""
            raise RuntimeError(f"mitmdump 启动失败，端口 {self.proxy_port} 未就绪: {err[:300]}")

        self._install_ca()
        self._set_system_proxy(True)
        logger.info(f"神策埋点抓包已启动，代理 127.0.0.1:{self.proxy_port}，事件文件: {self.events_file}")

    def stop(self):
        """还原系统代理并关闭 mitmdump"""
        try:
            self._set_system_proxy(False)
        except Exception as e:
            logger.warning(f"还原系统代理失败: {e}")
        if self._proc:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=8)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
            self._proc = None
        logger.info("神策埋点抓包已停止")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    # ---------- 事件查询 ----------

    def clear(self):
        """清空已捕获事件（在触发埋点前调用，以隔离单次断言）"""
        try:
            with open(self.events_file, "w", encoding="utf-8") as f:
                f.write("")
        except Exception:
            pass

    def get_events(self, event_name=None):
        """读取已捕获事件，可按事件名过滤"""
        events = []
        if not os.path.exists(self.events_file):
            return events
        with open(self.events_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                if event_name is None or ev.get("event") == event_name:
                    events.append(ev)
        return events

    def query_event(self, event_name):
        """查询某事件的所有上报记录"""
        data = self.get_events(event_name)
        logger.info(f"捕获到事件 [{event_name}] {len(data)} 条")
        return data

    def assert_event_reported(self, event_name, retries=10, interval=3):
        """
        断言某事件已上报（带重试，应对 SDK 批量上报延迟）
        :return: True 查询到记录；否则抛 AssertionError
        """
        for attempt in range(1, retries + 1):
            data = self.get_events(event_name)
            if data:
                logger.info(f"埋点验证通过: {event_name}（{len(data)} 条）")
                return True
            if attempt < retries:
                logger.info(f"未捕获到 [{event_name}]，第{attempt}次重试，{interval}s 后再查...")
                time.sleep(interval)
        raise AssertionError(f"埋点验证失败: 未捕获到事件 [{event_name}] 的上报记录")

    def assert_property(self, event_name, prop_key, prop_value=None, retries=10, interval=3):
        """
        断言某事件携带指定属性（可选断言属性值）
        """
        for attempt in range(1, retries + 1):
            for ev in self.get_events(event_name):
                props = ev.get("properties", {})
                if prop_key in props and (prop_value is None or props.get(prop_key) == prop_value):
                    logger.info(f"埋点属性验证通过: {event_name}.{prop_key}={props.get(prop_key)}")
                    return True
            if attempt < retries:
                time.sleep(interval)
        want = f"{prop_key}={prop_value}" if prop_value is not None else prop_key
        raise AssertionError(f"埋点属性验证失败: {event_name} 未包含 {want}")

    # ---------- 内部工具 ----------

    def _find_mitmdump(self):
        """定位 mitmdump 可执行路径；同时校验 mitmproxy 是否已安装"""
        try:
            import mitmproxy  # noqa: F401
        except ImportError:
            return None
        # 1. PATH 中查找
        path = shutil.which("mitmdump")
        if path:
            return path
        # 2. python 同级 Scripts 目录（Windows）
        scripts_dir = Path(sys.executable).parent / "Scripts"
        for name in ("mitmdump.exe", "mitmdump.bat", "mitmdump"):
            p = scripts_dir / name
            if p.exists():
                return str(p)
        # 3. venv 根目录
        for name in ("mitmdump.exe", "mitmdump"):
            p = Path(sys.executable).parent / name
            if p.exists():
                return str(p)
        return None

    def _wait_port_ready(self, timeout=20):
        end = time.time() + timeout
        while time.time() < end:
            try:
                with socket.create_connection(("127.0.0.1", self.proxy_port), timeout=1):
                    return True
            except OSError:
                if self._proc and self._proc.poll() is not None:
                    return False
                time.sleep(0.5)
        return False

    def _install_ca(self):
        """把 mitmproxy CA 证书安装到当前用户受信任根（免管理员）"""
        cer = Path.home() / ".mitmproxy" / "mitmproxy-ca-cert.cer"
        end = time.time() + 15
        while not cer.exists() and time.time() < end:
            time.sleep(0.5)
        if not cer.exists():
            logger.warning(f"未找到 mitmproxy CA 证书: {cer}，HTTPS 拦截可能失败")
            return
        try:
            r = subprocess.run(
                ["certutil", "-user", "-addstore", "Root", str(cer)],
                capture_output=True, text=True, encoding="gbk",
            )
            if r.returncode == 0:
                logger.info(f"已安装 mitmproxy CA 证书到当前用户根证书: {cer.name}")
            else:
                logger.warning(f"安装 CA 证书返回 {r.returncode}: {r.stderr.strip()[:200]}")
        except Exception as e:
            logger.warning(f"安装 CA 证书异常: {e}")

    def _set_system_proxy(self, enable):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _INET_KEY, 0, winreg.KEY_ALL_ACCESS)
        try:
            if enable:
                try:
                    self._saved_proxy = (
                        winreg.QueryValueEx(key, "ProxyEnable")[0],
                        winreg.QueryValueEx(key, "ProxyServer")[0],
                    )
                except FileNotFoundError:
                    self._saved_proxy = (0, "")
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ,
                                  f"127.0.0.1:{self.proxy_port}")
            else:
                enable_val, server_val = (self._saved_proxy or (0, ""))
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, enable_val)
                if server_val:
                    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, server_val)
        finally:
            winreg.CloseKey(key)
        self._notify_wininet()
        # 同步 WinHTTP 代理（部分应用使用 WinHTTP），失败可忽略
        try:
            if enable:
                subprocess.run(["netsh", "winhttp", "set", "proxy",
                                f"127.0.0.1:{self.proxy_port}"],
                               capture_output=True, text=True)
            else:
                subprocess.run(["netsh", "winhttp", "reset", "proxy"],
                               capture_output=True, text=True)
        except Exception:
            pass

    @staticmethod
    def _notify_wininet():
        """通知系统代理设置已变更，使应用立即生效"""
        try:
            import ctypes
            INTERNET_OPTION_SETTINGS_CHANGED = 39
            INTERNET_OPTION_REFRESH = 37
            internet = ctypes.windll.Wininet
            internet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            internet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
        except Exception:
            pass


if __name__ == "__main__":
    with SensorsCapture() as cap:
        logger.info("抓包运行中 30 秒，请在 VoiceWave 内操作以触发埋点...")
        time.sleep(30)
        logger.info(json.dumps(cap.get_events(), ensure_ascii=False, indent=2)[:2000])
