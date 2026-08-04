#!/usr/bin/python3
# -*- coding : utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn

"""
文件资源管理器自动化类（基于 uiautomation）
功能：
  - 启动文件资源管理器
  - 导航到指定路径
  - 关闭指定窗口
"""

import subprocess
import time
import uiautomation as auto
from commons.utils.myLogging import get_logger

logger = get_logger()


class FileExplorerAutomation:
    """
    封装 Windows 文件资源管理器的自动化操作。
    """

    def __init__(self, wait_timeout: int = 10):
        """
        初始化自动化控制器。

        参数:
            wait_timeout (int): 全局默认等待超时时间（秒），用于查找 UI 元素
        """
        self.wait_timeout = wait_timeout

    def open_and_navigate(self, target_path: str) -> bool:
        """
        启动文件资源管理器并导航到指定路径。

        参数:
            target_path (str): 目标路径，例如 r"F:\evwtools\Auto\导出路径"

        返回:
            bool: 成功返回 True，失败返回 False
        """
        try:
            # 启动 explorer.exe
            subprocess.Popen('explorer.exe')
            time.sleep(1)  # 等待进程初始化

            # 查找主窗口
            explorer_window = auto.WindowControl(searchDepth=1, ClassName='CabinetWClass')
            if not explorer_window.Exists(maxSearchSeconds=self.wait_timeout):
                logger.error("未在指定时间内找到文件资源管理器窗口。")
                return False

            explorer_window.SetActive()
            explorer_window.SetFocus()

            # 定位地址栏：优先使用结构路径，失败则兜底查找
            try:
                address_toolbar = (
                    explorer_window
                    .PaneControl(ClassName='WorkerW', searchDepth=1)
                    .PaneControl(ClassName='Address Band Root', searchDepth=2)
                    .ToolBarControl(ClassName='ToolbarWindow32', searchDepth=3)
                )
            except Exception:
                address_toolbar = explorer_window.ToolBarControl(ClassName='ToolbarWindow32', searchDepth=5)

            if not address_toolbar.Exists():
                logger.error("未找到地址栏控件。")
                return False

            address_toolbar.Click()
            time.sleep(0.3)

            # 输入路径并回车
            auto.SendKeys(target_path,interval=0.1,waitTime=0.2)
            auto.SendKeys('{Enter}')
            time.sleep(1)

            logger.info(f"已成功导航到路径: {target_path}")
            return True

        except Exception as e:
            logger.error(f"导航过程中发生错误: {e}")
            return False

    def close_window(self, window_title: str = None) -> bool:
        """
        关闭文件资源管理器窗口。

        参数:
            window_title (str or None): 窗口标题（如“导出路径”）。若为 None，则关闭任意 CabinetWClass 窗口。

        返回:
            bool: 成功关闭返回 True，否则 False
        """
        try:
            if window_title:
                window = auto.WindowControl(
                    Name=window_title,
                    ClassName='CabinetWClass',
                    searchDepth=1
                )
            else:
                window = auto.WindowControl(
                    ClassName='CabinetWClass',
                    searchDepth=1
                )

            if not window.Exists(maxSearchSeconds=self.wait_timeout):
                logger.error("未找到要关闭的文件资源管理器窗口。")
                return False

            # 尝试点击标题栏的“关闭”按钮
            close_btn = window.TitleBarControl(AutomationId='TitleBar').ButtonControl(Name='关闭')
            if close_btn.Exists():
                close_btn.Click()
                logger.info("已关闭文件资源管理器窗口。")
                return True


        except Exception as e:
            logger.error(f"关闭窗口时发生错误: {e}")
            return False



if __name__ == '__main__':
    # auto.WindowControl(Name='导出路径', ClassName='CabinetWClass', Depth=1).PaneControl(ClassName='WorkerW',
    #                                                                                 Depth=1).PaneControl(
    #     ClassName='Address Band Root', Depth=2).ToolBarControl(Name='地址: F:\evwtools\Auto\导出路径',
    #                                                            ClassName='ToolbarWindow32', Depth=3)
    #
    logger.info("111")