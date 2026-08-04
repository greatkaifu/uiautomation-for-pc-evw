#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn

"""
任务管理器自动化助手（支持自动提权）
"""

import os
import sys
import signal
import subprocess
import ctypes
import uiautomation as auto
from commons.utils.myLogging import get_logger

logger = get_logger()


class TaskManagerHelper:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @staticmethod
    def is_admin() -> bool:
        """检查当前是否以管理员身份运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def run_as_admin():
        """以管理员身份重新启动当前脚本"""
        if not TaskManagerHelper.is_admin():
            logger.info("检测到非管理员权限，正在尝试提权...")
            try:
                # 重新启动当前脚本并请求管理员权限
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit(0)  # 退出当前非管理员实例
            except Exception as e:
                logger.error(f"提权失败: {e}")
                logger.info("请手动以管理员身份运行此脚本")
                sys.exit(1)

    def open_task_manager(self, switch_to_details: bool = True):
        """启动任务管理器并切换到'详细信息'页"""
        logger.info("正在启动任务管理器...")
        subprocess.Popen('taskmgr')

        if switch_to_details:
            taskmgr = auto.WindowControl(
                searchDepth=1,
                Name='任务管理器',
                ClassName='TaskManagerWindow'
            )
            if taskmgr.Exists(maxSearchSeconds=self.timeout):
                # 尝试查找"详细信息"标签
                details_tab = taskmgr.TabItemControl(Name='详细信息')
                if details_tab.Exists(maxSearchSeconds=2):
                    details_tab.Click()
                    logger.info("已切换到'详细信息'标签页")
                else:
                    logger.info("未找到'详细信息'标签，可能已在当前页")

    def get_process_pid(self, process_name: str) -> int:
        """
        从任务管理器获取指定进程的 PID
        :return: PID 字符串（如 '9060'）
        """
        logger.info(f"正在查找任务管理器窗口...")
        taskmgr = auto.WindowControl(
            searchDepth=1,
            Name='任务管理器',
            ClassName='TaskManagerWindow'
        )
        if not taskmgr.Exists(maxSearchSeconds=self.timeout):
            raise RuntimeError("任务管理器窗口未找到")

        # 查找数据表格（兼容不同 Windows 版本）
        table_pane = None
        for name in ['表格', '进程', 'Processes']:  # 多语言支持
            table_pane = taskmgr.PaneControl(Name=name, ClassName='Page')
            if table_pane.Exists(maxSearchSeconds=1):
                break
        if not table_pane or not table_pane.Exists():
            raise RuntimeError("未找到任务管理器中的数据表格")

        logger.info(f"正在定位进程: {process_name} ...")
        target_item = table_pane.ListItemControl(Name=process_name)
        if not target_item.Exists(maxSearchSeconds=self.timeout):
            raise RuntimeError(f"未找到进程: {process_name}")

        # 提取所有文本
        texts = []
        for child in target_item.GetChildren():
            if child.ControlType == auto.ControlType.TextControl:
                name = child.Name
                if name and name.strip():
                    texts.append(name.strip())

        if len(texts) < 2:
            raise RuntimeError(f"进程 {process_name} 的数据格式异常")

        pid_str = texts[1]  # 第二个字段通常是 PID
        logger.info(f"找到进程 {process_name}，PID: {pid_str}")
        return int(pid_str)

    def kill_process(self, pid: int) -> bool:
        """根据 PID 终止进程"""
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info(f"成功终止进程 PID: {pid}")
            return True
        except ProcessLookupError:
            logger.error(f"进程 {pid} 不存在")
            return False
        except PermissionError:
            logger.error(f"权限不足，无法终止进程 {pid}")
            logger.info("建议：以管理员身份运行脚本")
            return False
        except Exception as e:
            logger.error(f"终止进程时发生错误: {e}")
            return False



if __name__ == "__main__":

    # 赋予管理权限
    TaskManagerHelper.run_as_admin()
    # 实例化对象
    helper = TaskManagerHelper()

    try:
        # 打开任务管理器
        helper.open_task_manager()

        # 直接通过进程名终止（推荐方式）
        pid = helper.get_process_pid('easeus.voicewave.exe')

        helper.kill_process(pid)
    except Exception as e:
        logger.error(f"操作失败: {e}")