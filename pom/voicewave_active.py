#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_active.py
from bases.basePage import BasePage
import uiautomation as auto
from commons.utils.myLogging import get_logger

logger = get_logger()


class Active(BasePage):


    def __int__(self, main_window):
        BasePage.__init__(self, main_window)



    def find_olduser_start_alert(self):
        """
        未激活老用户启动弹窗
        在ini配置文件，修改时间  字段   NEW_USER_LAUNCH_TIME=
        :return:
        """
        alert_text = self.main_window.GroupControl(ClassName='SuperPrizeWidget', Depth=1).GroupControl(
            ClassName='QWidget', AutomationId='FramelessWidget.SuperPrizeWidget.widget_2', Depth=1).ButtonControl(
            Name='Claim Now', ClassName='QPushButton', Depth=1)

        # 等待按钮出现
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None

