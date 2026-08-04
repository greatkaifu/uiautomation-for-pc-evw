#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : viocewave_discount _alert.py


import time

from bases.basePage import BasePage

import uiautomation as auto

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger

logger = get_logger()


class DiscountAlert(BasePage):
    """
    EaseUS VoiceWave 启动提示弹窗
    """

    def __int__(self, main_window):
        BasePage.__init__(self, main_window)


    #==============================================================未激活的老用户=======================================================
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

    def close_olduser_start_alert(self):

        control=self.main_window.GroupControl(ClassName='SuperPrizeWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        if auto.WaitForExist(control, 1):
            # 继承BasePage
            BasePage.click(self, control)
            logger.info(f"已点击关闭当前弹窗")
            time.sleep(1)
        else:
            logger.info(f"启动弹窗未出现")

    def find_olduser_Wait_alert(self):
        """
        未激活老用户关闭程序后弹出的挽留弹窗
        :return:
        """

        alert_text=self.main_window.GroupControl(ClassName='LimitedTimeDiscountWidget', Depth=1).TextControl(Name='Limited Time Offer', ClassName='QLabel', Depth=2)
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None




    def close_olduser_Wait_alert(self):
        """
        挽留弹窗
        :return:
        """
        control=self.main_window.GroupControl(
            ClassName='LimitedTimeDiscountWidget', Depth=1).GroupControl(ClassName='QWidget',
                                                                         AutomationId='FramelessWidget.LimitedTimeDiscountWidget.widget_7',
                                                                         Depth=1).ButtonControl(ClassName='QPushButton',
                                                                                                Depth=1)
        # 继承BasePage
        BasePage.click(self, control)
        logger.info(f"已点击关闭当前挽留弹窗")


    #==============================================================未激活的新用户=======================================================

    def find_newuser_Wait_alert_first(self):
        """
        未激活新用户关闭程序，挽留弹窗,,没见过内购激活弹窗，也没有点击过buy now按钮

        :return:
        """
        alert_text = self.main_window.GroupControl(ClassName='LimitedTimeDiscountWidget', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.LimitedTimeDiscountWidget.widget_4', Depth=1).TextControl(Name='Original Price', ClassName='QLabel', Depth=1)
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None


    def find_newuser_Wait_alert_second(self):
        """
        未激活新用户关闭程序，挽留弹窗
        第二类：未激活,但点击过常规购买按钮(进入内购激活弹窗页，并且点击“buy now”按钮后，进入购物车)的用户，在关闭程序时弹出的挽留折扣弹窗
        :return:
        """
        alert_text = self.main_window.GroupControl(ClassName='DiscountCard3', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DiscountCard3.widget_2', Depth=1).TextControl(Name='I don’t care', ClassName='QLabel', Depth=1)

        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None

    def find_newuser_start_alert(self):
        """
        未激活新用户启动弹窗
        :return:
        """
        alert_text = self.main_window.GroupControl(ClassName='DiscountCard1', Depth=1).GroupControl(ClassName='QWidget',
                                                                                                    AutomationId='FramelessWidget.DiscountCard1.widget_2',
                                                                                                    Depth=1).TextControl(
            Name='Pro Bonus Bundle', ClassName='QLabel', Depth=3)

        # 等待按钮出现
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None

    def close_newuser_start_alert(self):
        """
        关闭第一种新用户启动弹窗
        """
        control = self.main_window.GroupControl(ClassName='DiscountCard1', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=1)
        if auto.WaitForExist(control, 1):
            # 继承BasePage
            BasePage.click(self, control)
            logger.info(f"已点击关闭当前弹窗")
            time.sleep(1)
            return True
        else:
            logger.info(f"启动弹窗未出现")
            return False

    def close_newuser_wait_start_alert_first(self):
        """
          未激活的新用户第一类挽留弹窗，未激活新用户没有看过价格弹窗
          :return:
        """
        control = self.main_window.GroupControl(
            ClassName='LimitedTimeDiscountWidget', Depth=1).GroupControl(ClassName='QWidget',
                                                                         AutomationId='FramelessWidget.LimitedTimeDiscountWidget.widget_7',
                                                                         Depth=1).ButtonControl(ClassName='QPushButton',
                                                                                                Depth=1)
        # 继承BasePage
        BasePage.click(self, control)
        logger.info(f"已点击关闭当前挽留弹窗")

    def close_newuser_wait_alert_second(self):
        """
        未激活新用户关闭程序，挽留弹窗
        第二类：未激活,进入内购激活弹窗页，但是未点击过“buy now”按钮后，在关闭程序时弹出的挽留折扣弹窗
        关闭第二类挽留弹窗
        :return:
        """
        control = self.main_window.GroupControl(ClassName='DiscountCard2', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DiscountCard2.widget_5', Depth=1).TextControl(Name='Exit Anyway', ClassName='QLabel', Depth=1)
         # 继承BasePage
        BasePage.click(self, control)
        logger.info(f"已点击关闭当前挽留弹窗")

    def close_newuser_wait_alert_by_picture(self, path, x, y):
        """
        为了测试多言，通过图片识别处理
        公共方法
        center: 查找图片的中心点坐标
        相对于图片的中心偏移量计算出目标坐标点

        """
        projectroot=GetPath()
        template_path = path
        try:
            # 拼接完整图片路径（字符串）
            position = ScreenElement(projectroot.getImagePath(template_path))
            # # 找到该图标，点击操作
            # position.click(delay=1)
            if position.exists():
                # 计算找到图标的坐标，相对位置点击
                position.click_relative_to_element(offset_x=x, offset_y=y)

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {projectroot.getImagePath(template_path)} 图标")


    def close_newuser_wait_alert_third(self):
        """
        未激活新用户关闭程序，挽留弹窗
        第三类：未激活,进入内购激活弹窗页，但是未点击过“buy now”按钮后，在关闭程序时弹出的挽留折扣弹窗
        关闭第二类挽留弹窗
        :return:
        """
        control = self.main_window.GroupControl(ClassName='DiscountCard3', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DiscountCard3.widget_2', Depth=1).TextControl(Name='I don’t care', ClassName='QLabel', Depth=1)
        if auto.WaitForExist(control, 1):
            # 继承BasePage
            BasePage.click(self, control)
            logger.info(f"已点击关闭当前挽留弹窗")
            return True
        else:
            logger.info(f"未激活新用户关闭程序，挽留弹窗未出现")
            return None


    def find_newuser_wait_alert_third(self):
        """
        未激活新用户关闭程序，挽留弹窗
        第三类：未激活，进入内购激活弹窗页，并且点击“buy now”按钮后，进入购物车的用户，在关闭程序时弹出的挽留折扣弹窗
        :return:
        """
        alert_text = self.main_window.GroupControl(ClassName='DiscountCard2', Depth=1).GroupControl(ClassName='QWidget',
                                                                                                    AutomationId='FramelessWidget.DiscountCard2.widget_5',
                                                                                                    Depth=1).TextControl(
            Name='Exit Anyway', ClassName='QLabel', Depth=1)
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None









