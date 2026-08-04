#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : languageSet.py

import os
from datetime import datetime

from PIL import ImageGrab
# 具体页面（业务封装）
import subprocess
import time

import uiautomation as auto
from commons.utils.myLogging import get_logger
# 配置日志
logger = get_logger()

class  LanguageSet:
    """多语言设置"""

    def __init__(self):
        """
        control窗口，在注册表设置多语言
        """
        pass

    def open_run_dialog(self):
        # 等待一下，确保系统准备好接收输入
        time.sleep(0.5)

        # 方式 1: 使用 {Win} + r
        auto.SendKeys('{Win}r', waitTime=0.1)

        # 方式 2: 使用 # 代表 Win 键 (效果相同)
        # auto.SendKeys('#r', waitTime=0.1)

        logger.info("已发送 Win+R 快捷键")



    def _continuous_backspace(slef,duration=10, interval=0.05):
        """持续发送 Backspace 按键指定时长"""
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration:
            auto.SendKeys('{Backspace}')
            count += 1
            time.sleep(interval)
        logger.info(f"完成，共删除 {count} 次，耗时 {duration} 秒")

    import uiautomation as auto
    import time

    def _hold_backspace_with_window(self, duration=20, interval=0.05):
        """
        激活指定窗口后持续发送 Backspace
        :param window_name: 窗口标题（支持模糊匹配）
        :param duration: 持续时间（秒）
        :param interval: 按键间隔（秒）
        """
        window_name = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit', Depth=1)
        logger.info(f"查找窗口：{window_name}")

        # 查找并激活窗口
        window = auto.WindowControl(searchName=window_name)
        if not window.Exists(maxSearchSeconds=5):
            logger.error(f"未找到窗口：{window_name}")
            return False

        window.SetActive()
        window.SetFocus()
        time.sleep(0.5)  # 等待窗口就绪
        logger.info(f"窗口已激活：{window_name}")
        # 注册表编辑页面
        control = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit', Depth=1).EditControl(ClassName='Edit',
                                                                                                      Depth=1)
        control.DoubleClick()
        # 持续发送 Backspace
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration:
            auto.SendKeys('{Backspace}')
            count += 1
            time.sleep(interval)

        elapsed = time.time() - start_time
        logger.info(f"完成，共删除 {count} 次，耗时 {elapsed:.2f} 秒")
        return True



    def open_and_control_regedit(self, language):
        # 1. 启动 regedit (如果尚未启动)
        # 注意：regedit 通常需要管理员权限，建议以管理员身份运行此 Python 脚本
        try:
            self.open_run_dialog()
            # 检查是否已经存在 control窗口
            control_window = auto.WindowControl(Name='运行', ClassName='#32770', Depth=1).EditControl(Name='打开(O):',
                                                                                                    ClassName='Edit',
                                                                                                    Depth=2)
            if control_window.Exists(maxSearchSeconds=5):
                logger.info(f"{control_window.Name}已经查找到")
                control_window.SetFocus()  # 获取焦点
                control_window.Click()
                auto.SendKeys('{Ctrl}{A}')  # 全选
                auto.SendKeys('{Delete}')  # 删除
                auto.SendKeys("regedit", waitTime=0.5)
                auto.SendKeys('{Enter}', waitTime=0.5)
                # 等注册窗口加载.....
                time.sleep(2)
                # 注册表编辑页面
                control = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit', Depth=1).EditControl(
                    ClassName='Edit',
                    Depth=1)
                control.Click()
                auto.SendKeys('{Ctrl}{A}', waitTime=0.5)  # 全选
                auto.SendKeys('{Ctrl}{A}', waitTime=0.5)  # 全选
                auto.SendKeys('{Delete}')
                time.sleep(3)
                auto.SendKeys("计算机\HKEY_LOCAL_MACHINE\SOFTWARE\EaseUS\EVW")
                auto.SendKeys('{Enter}', waitTime=0.5)
                evw_regedit = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit', Depth=1).ListControl(
                ClassName='SysListView32', Depth=1).ListItemControl(Name='Language', Depth=1).EditControl(
                Name='Language', Depth=1)
                if evw_regedit.Exists(maxSearchSeconds=5):
                    logger.info(f"{evw_regedit.Name}已经查找到")
                    evw_regedit.DoubleClick()
                    control = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit', Depth=1).EditControl(
                        Name='数值数据(V):', ClassName='Edit', Depth=2)

                    control = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit', Depth=1).EditControl(
                        Name='数值数据(V):', ClassName='Edit', Depth=2)
                    if control.Exists(maxSearchSeconds=5):
                        logger.info(f"{control.Name}已经查找到")
                        control.Click()
                        auto.SendKeys('{Ctrl}{A}')  # 全选
                        auto.SendKeys('{Delete}')  # 删除
                        auto.SendKeys(language, waitTime=0.5)
                        control_btn = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit',
                                                         Depth=1).ButtonControl(Name='确定', ClassName='Button',
                                                                                Depth=2)
                        if control_btn.Exists(maxSearchSeconds=5):
                            logger.info(f"{control_btn.Name}已经查找到")
                            control_btn.Click()
                            time.sleep(1)
                            logger.info("修改成功")
                            close_btn = auto.WindowControl(Name='注册表编辑器', ClassName='RegEdit_RegEdit',
                                                           Depth=1).TitleBarControl(Depth=1).ButtonControl(
                                Name='关闭', Depth=1)
                            # 关闭注册表页面
                            close_btn.Click()
                            return True
            else:
                logger.error(" 超时：未找到control窗口")
                return None


        except Exception as e:
            logger.error(f"启动失败：{e}")
            return None

