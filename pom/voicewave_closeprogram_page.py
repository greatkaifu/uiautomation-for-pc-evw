#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_closeprogram_page.py

# 具体页面（业务封装）
import subprocess
import time
from bases.basePage import BasePage
import uiautomation as auto
from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger
from commons.utils.readconfig import INIConfigReader

logger = get_logger()


class CloseProgram(BasePage):
    """
    关闭程序
    """
    def __int__(self, main_window):
        super().__init__(main_window)



    def close_program(self):
        """
        关闭 EVW 程序
        :return:
        """

        logger.info("点击按钮")
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='QPushButton',
            AutomationId='FramelessWidget.MainWidgetTitle.widget_title.widget_btnGrp.btn_close',
            Depth=3)
        BasePage.click(self, control)
        logger.info("已点击程序关闭按钮")
        time.sleep(1)
        # kill_process_by_name("easeus.voicewave.exe")

    @staticmethod
    def start_program():
        """
        启动EVW程序
        :return:
        """
        logger.info("启动程序")
        # 注意是在English环境下调试的代码，注意程序安装语言环境是English
        read = INIConfigReader()
        program_path = read.getconfig("install", "path")
        # 启动程序
        logger.info("正在启动 EaseUS VoiceWave...")
        subprocess.Popen(program_path)

        # 等待主窗口出现（最多 30 秒）
        logger.info("等待主窗口加载...")
        main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
        if not main_win.Exists(maxSearchSeconds=30):
            logger.error("未能在 20 秒内找到主窗口，脚本退出。")
            exit(1)


    def click_program_ok(self):
        """
        关闭程序的二次确认弹窗，点击OK确定按钮，关闭程序
        :return:
        """

        # 弹出二次确认弹窗，点击OK确定按钮，关闭程序
        control = self.main_window.GroupControl(ClassName='CExitWindowPage', Depth=1).ButtonControl(Name='OK',
                                                                                                      ClassName='CustomBtn',
                                                                                                      Depth=1)
        # 设置一个时间内查找到控件
        BasePage.click(self,control)
    def find_program_exit_icon(self):
        """
        查找程序退出图标
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/ok.png"

            position = ScreenElement(GetPath().getImagePath(template_path))
            position.exists()
            logger.info("=================" + str(position.exists()))
            return position.exists()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {GetPath().getImagePath(template_path)} 图标")
            return False

    def select_exit_way(self):
        """
        选择退出程序方式
        :return:
        """
        # 选择退出方式
        control = self.main_window.GroupControl(ClassName='CExitWindowPage', Depth=1).RadioButtonControl(
            Name='Exit VoiceWave', ClassName='QRadioButton', Depth=2)

        BasePage.click(self, control)

    def select_minimize_way(self):
        """
        选择最小化方式
        :return:
        """

        control = self.main_window.GroupControl(ClassName='CExitWindowPage', Depth=1).RadioButtonControl(Name='Minimize to tray', ClassName='QRadioButton', Depth=2)
        BasePage.click(self, control)
        logger.info(f"已选择最小化方式。")
    def close_exit_alert_btn(self):
        """
        点击退出程序，二次确认弹窗的关闭按钮
        """
        control=self.main_window.GroupControl(ClassName='CExitWindowPage', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        if BasePage.find_control(self,control):
            BasePage.click(self,control)
            logger.info(f"已经关闭退出程序二次确认弹窗。")
        logger.info(f"未查找到退出程序二次确认弹窗。")