#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : installprogram.py

# silent_installer.py
import subprocess
import time
from pathlib import Path

# installer_utils.py
import subprocess
import sys
import ctypes
import os

from commons.utils.myLogging import get_logger

logger = get_logger()



class SilentInstaller:


    def __init__(self, exe_path, lang='zh', custom_args=None, timeout=600):
        """
        :param exe_path: 安装程序路径
        :param lang: 语言代码 'zh' 或 'en'
        :param custom_args: 额外参数列表，如 ['/DIR=C:\\Program Files\\MyApp']
        :param timeout: 安装超时时间（秒）
        """
        self.exe_path = Path(exe_path).resolve()
        self.lang = lang
        self.custom_args = custom_args
        self.timeout = timeout
        self.LANGUAGE_MAP = {
            'zh': {
                'inno': 'zh_CN',  # Inno Setup 语言ID
                'installshield': '2052',  # InstallShield LANG=2052 (简体中文)
                'display': '简体中文'
            },
            'en': {
                'inno': 'English',
                'installshield': '1033',
                'display': 'English'
            }
        }


        if not self.exe_path.exists():
            raise FileNotFoundError(f"安装程序不存在: {self.exe_path}")

        # 自动提权
        self.run_as_admin()
        logger.info(f"当前权限: {'管理员' if self.is_admin() else '普通用户'}")



    def is_admin(self):
        """检查是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_as_admin(self):
        """以管理员身份重启脚本"""
        if not self.is_admin():
            logger.warning("未检测到管理员权限，尝试提权...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)

    def detect_installer_type(self):
        """自动识别安装包类型"""
        try:
            output = subprocess.check_output(
                ['findstr', '/i', 'inno setup', self.exe_path],
                stderr=subprocess.DEVNULL,
                shell=True
            ).decode('gbk', errors='ignore')
            if 'inno' in output.lower():
                return 'inno'
        except:
            pass

        # 备用方案：根据文件特征判断
        filename = os.path.basename(self.exe_path).lower()
        if 'setup' in filename or 'install' in filename:
            return 'generic'  # 通用静默参数
        return 'unknown'

    def build_silent_args(self,installer_type, lang_code='zh', custom_args=None):
        """根据安装器类型和语言生成静默参数"""

        lang_cfg = self.LANGUAGE_MAP.get(lang_code, self.LANGUAGE_MAP['zh'])
        args = []

        if installer_type == 'inno':
            args = ['/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART']
            if lang_cfg.get('inno'):
                args.append(f'/LANG={lang_cfg["inno"]}')

        elif installer_type == 'nsis':
            args = ['/S']  # NSIS 通常不支持运行时切换语言

        elif installer_type == 'installshield':
            args = ['/s']
            lang_id = lang_cfg.get('installshield', '2052')
            args.append(f'/v"/qn LANG={lang_id}"')

        elif installer_type == 'generic':
            # 尝试通用静默参数
            args = ['/S', '/silent', '/quiet', '/qn']

        # 合并自定义参数
        if custom_args:
            args.extend(custom_args if isinstance(custom_args, list) else [custom_args])

        return args

    def install(self):
        """执行静默安装"""
        installer_type = str(self.detect_installer_type())
        logger.info(f"检测到安装包类型: {installer_type}")

        args = self.build_silent_args(installer_type, self.lang, self.custom_args)
        cmd = [str(self.exe_path)] + args

        logger.info(f"执行命令: {' '.join(cmd)}")

        try:
            # 使用GBK编码避免中文乱码
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='gbk',
                creationflags=subprocess.CREATE_NO_WINDOW  # 隐藏控制台窗口
            )

            # 简单进度监控（根据实际需求可扩展）
            start_time = time.time()
            while process.poll() is None:
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0:
                    logger.info(f"安装进行中... 已运行 {elapsed} 秒")
                time.sleep(5)

                if elapsed > self.timeout:
                    process.terminate()
                    raise TimeoutError(f"安装超时（>{self.timeout}秒）")

            stdout, _ = process.communicate()
            if stdout:
                logger.debug(f"安装输出:\n{stdout}")

            if process.returncode == 0:
                logger.info("安装成功完成")
                return True
            else:
                logger.error(f"安装失败，退出码: {process.returncode}")
                return False

        except Exception as e:
            logger.exception(f"安装过程异常: {e}")
            return False


# ===== 使用示例 =====
if __name__ == "__main__":
    installer = SilentInstaller(
        exe_path=r"C:\Users\admin\Desktop\EVW\3.3.3\2026-02-09_09.22\free\voice_wave.exe",
        lang='en',  # 可切换为 'en'
        custom_args=[
            '/DIR=C:\\Program Files\\EaseUS\\VoiceWave',
            '/NOICONS'  # 不创建桌面快捷方式（Inno参数）
        ],
        timeout=300
    )
    success = installer.install()
    exit(0 if success else 1)

