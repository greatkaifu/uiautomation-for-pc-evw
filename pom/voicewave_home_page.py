#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_home_page.py.py

# 具体页面（业务封装）
import subprocess
import time

from bases.basePage import BasePage

import uiautomation as auto

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.killProcess import kill_process_by_name
from commons.utils.readconfig import INIConfigReader
from commons.utils.targetNotFoundError import TargetElementNotFoundError
from commons.utils.myLogging import get_logger

logger = get_logger()

project_root = GetPath()


class VoiceWavePage(BasePage):
    """EaseUS VoiceWave 主界面操作封装"""

    def __int__(self, main_window):
        super().__init__(main_window)

    def click_login_title(self):
        """
        在title栏，点击用户登录入口
        :return:
        """
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='UserAvatarButton', Depth=3)
        if auto.WaitForExist(control, 5):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击title栏，登录入口")
            return True
        else:
            logger.info(f"未找到登录入口")
            return None

    def close_login_wait_alert(self):
        """
        关闭登录等待弹窗
        :return:
        """
        control = self.main_window.GroupControl(ClassName='LoginStatusDialog', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=1)
        if auto.WaitForExist(control, 5):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击登录等待弹窗关闭按钮")
            return True
        else:
            logger.info(f"未找到登录等待弹窗的关闭按钮")
            return None

    def find_start_alert(self):
        """
        获取导航列表
        :return:
        """
        alert_text = self.main_window.GroupControl(
            ClassName='DiscountCard1', Depth=1).GroupControl(ClassName='QWidget',
                                                             AutomationId='FramelessWidget.DiscountCard1.widget_2',
                                                             Depth=1).TextControl(Name='Pro Bonus Bundle',
                                                                                  ClassName='QLabel', Depth=3)
        # 等待按钮出现
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return alert_text.Name
        else:
            logger.info(f"激活弹窗未出现")
            return None

    def close_start_alert_off(self):
        """
        未激活用户首次启动，弹出启动折扣弹窗，关闭未启动折扣弹窗
        :return:
        """

        control = self.main_window.GroupControl(
            ClassName='DiscountCard1', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        # 继承
        BasePage.click(self, control)

        logger.info(f"关闭未激活新用户首次启动折扣弹窗")

    def close_active_alert(self):
        """
        关闭激活弹窗
        :return:
        """
        control = self.main_window.GroupControl(ClassName='UpgradeWidget', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=1)
        # .GroupControl(ClassName='UserCenterWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        # 继承BasePage
        VoiceWavePage.click(self, control)
        logger.info(f"已点击关闭当前活动提示框")

    def find_is_active_alert(self):
        """
        查找当前活动提示框是否存在
        :return:
        """
        alert_text = self.main_window.GroupControl(ClassName='UpgradeWidget', Depth=1).TextControl(
            Name='Get Pro to Enjoy More Features', ClassName='QLabel', Depth=3)
        # 等待按钮出现
        if auto.WaitForExist(alert_text, 1):
            logger.info(f"激活弹窗已经出现: {alert_text.Name}")
            return True
        else:
            logger.info(f"激活弹窗未出现")
            return False

    def upgrade_click(self):
        """
        在title栏，点击upgrade按钮，弹出限制激活弹窗
        升级按钮  VoiceWave
        :return:
        """
        control = self.main_window.GroupControl(
            ClassName='MainWidgetTitle', Depth=1).ButtonControl(ClassName='CIconButton', Depth=3)
        # 等待按钮出现
        VoiceWavePage.click(self, control)

        logger.info(f"已点击进入 upgrade 功能。")

    def click_buy_now(self):
        """
        在限制激活弹窗，点击购买按钮
        """
        control = self.main_window.GroupControl(ClassName='UpgradeWidget', Depth=1).GroupControl(ClassName='QWidget',
                                                                                                 AutomationId='FramelessWidget.UpgradeWidget.widget_3',
                                                                                                 Depth=1).GroupControl(
            ClassName='QWidget', Depth=2).GroupControl(ClassName='UpgradePriceItemWidget', Depth=1).GroupControl(
            ClassName='QWidget',
            AutomationId='FramelessWidget.UpgradeWidget.widget_3.widget_20.widget_18.widget_21.widget_5',
            Depth=1).GroupControl(ClassName='QWidget', Depth=1)
        #
        VoiceWavePage.click(self, control)
        logger.info(f"已点击进入购物车页。")

    def nav1_save_setting(self):
        """
        获取导航列表
        :return:
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget',
                                                                                                   AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.SoundLayoutWidget.widget_itemInfoCtl',
                                                                                                   Depth=2).GroupControl(
            ClassName='QScrollArea', Depth=4).ButtonControl(Name='Save settings', ClassName='CustomBtn', Depth=4)
        # 继承
        VoiceWavePage.click(self, control)

        logger.info(f"已点击进入 soundboard 功能。")

    # 左侧导航栏

    def nav1_realtime_voice_changer(self):
        """
        获取导航列表
        :return:
        """
        control = self.main_window.ListControl(ClassName='CNaviListWidget', Depth=5).ListItemControl(Depth=1)
        # 继承
        BasePage.click(self, control)

        logger.info(f"已点击进入 soundboard 功能。")

    def nav2_soundboard(self):
        """
        获取导航列表
        :return:
        """

        control = self.main_window.ListControl(
            ClassName='CNaviListWidget', Depth=5).ListItemControl(foundIndex=2, Depth=1)
        # 继承
        VoiceWavePage.click(self, control)
        logger.info(f"已点击进入 soundboard 功能。")

    def nav3_community_library(self):
        """
        获取导航列表
        :return:
        """
        # 等待按钮出现
        control = self.main_window.ListControl(ClassName='CNaviListWidget', Depth=5).ListItemControl(foundIndex=3,
                                                                                                     Depth=1)
        # 继承
        VoiceWavePage.click(self, control)

        logger.info(f"已点击进入 soundboard 功能。")

    def nav4_file_voice_changer(self):
        """
        获取导航列表  文件模式
        :return:
        """
        control = self.main_window.ListControl(
            ClassName='CNaviListWidget', Depth=5).ListItemControl(foundIndex=4, Depth=1)
        # 继承
        BasePage.click(self, control)

        logger.info(f"已点击进入 soundboard 功能。")

    def nav5_voice_creation(self):
        """
        获取导航列表  克隆功能
        :return:
        """
        control = self.main_window.ListControl(
            ClassName='CNaviListWidget', Depth=5).ListItemControl(foundIndex=5, Depth=1)
        # 继承
        BasePage.click(self, control)

        logger.info(f"已点击进入 soundboard 功能。")

    def nav6_setting(self):
        """
        获取导航列表  设置功能
        :return:
        """
        control = self.main_window.ListControl(
            ClassName='CNaviListWidget', Depth=5).ListItemControl(foundIndex=6, Depth=1)

        # 继承
        BasePage.click(self, control)

        logger.info(f"已点击进入 setting 功能。")

    def click_close_program_btn(self):
        """
        在title栏，点击关闭程序按钮
        :return:
        """
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).GroupControl(
            ClassName='QWidget', Depth=2).ButtonControl(ClassName='QPushButton', foundIndex=6, Depth=1)
        BasePage.click(self, control)
        logger.info(f"已点击关闭程序按钮")

    def new_off(self):
        """

        :return:
        """

        control = self.main_window.GroupControl(
            ClassName='DiscountCard2', Depth=1).GroupControl(ClassName='QWidget',
                                                             AutomationId='FramelessWidget.DiscountCard2.widget_5',
                                                             Depth=1).TextControl(Name='Exit Anyway',
                                                                                  ClassName='QLabel',
                                                                                  Depth=1)
        # 继承
        VoiceWavePage.click(self, control)

        logger.info(f"已点击进入  功能。")

    def click_title_edit(self):
        """
        关闭程序的二次确认弹窗，点击OK确定按钮，关闭程序
        :return:
        """

        # 弹出二次确认弹窗，点击OK确定按钮，关闭程序
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='QPushButton',
            AutomationId='FramelessWidget.MainWidgetTitle.widget_title.widget_btnGrp.btn_userQuestion', Depth=3)
        # 设置一个时间内查找到控件
        BasePage.click(self, control)

    def click_title_discord_icon(self):
        """
            在title栏，点击discord图标
        :return:
        """

        #
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=3)
        # 设置一个时间内查找到控件
        BasePage.click(self, control)

    def click_title_youtube_icon(self):
        """
        在title栏，点击youtobe图标
        :return:
        """

        #
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='QPushButton',
            AutomationId='FramelessWidget.MainWidgetTitle.widget_title.widget_btnGrp.btn_youtube', Depth=3)
        # 继承
        VoiceWavePage.click(self, control)

    def click_title_max_icon(self):
        """
        在title栏，点击github图标
        :return:
        """

        #
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).CheckBoxControl(
            ClassName='QPushButton', Depth=3)
        # 设置一个时间内查找到控件
        BasePage.click(self, control)

    def find_title_max_icon(self):
        """
        在title栏，查找最
        :return:
        """
        project_path = GetPath()
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/max.png"

            position = ScreenElement(project_path.getImagePath(template_path))
            position.exists()
            logger.info("=================" + str(position.exists()))
            return position.exists()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_path.getImagePath(template_path)} 图标")

    def click_title_min_icon(self):
        """
        在title栏，点击github图标
        :return:
        """

        #
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='QPushButton', AutomationId='FramelessWidget.MainWidgetTitle.widget_title.widget_btnGrp.btn_min',
            Depth=3)
        # 设置一个时间内查找到控件
        BasePage.click(self, control)

    def find_title_min_icon(self):
        """
        在title栏，点击最小化按钮，此时应该是找不到程序的log图标；
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/log.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            position.exists()
            logger.info("=================" + str(position.exists()))
            return position.exists()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")
            return False

    def click_title_setting_icon(self):
        """
        在title栏,点击设置图标
        :return:
        """
        #
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(
            ClassName='QPushButton', AutomationId='FramelessWidget.MainWidgetTitle.widget_title.widget_btnGrp.btn_menu',
            Depth=3)
        # 继承
        BasePage.click(self, control)

    def click_title_1_icon(self):
        """
        在title栏,点击设置菜单栏第1个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/close_btn.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click(delay=2)
        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def click_title_2_icon(self):
        """
        在title栏,点击设置菜单栏第2个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/2.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def find_title_2_alert(self):
        """
        在title栏,点击第二个功能，弹出的一个弹窗，获取弹窗上的文本，表示该弹窗出现
        :return:
        """
        # 弹窗上的文本的控件地址
        control = self.main_window.GroupControl(ClassName='OptimizeTips', Depth=1).TextControl(
            Name='Optimize the VoiceWave experience in Discord', ClassName='QLabel', Depth=1)

        if BasePage.find_control_text(self, control, "Optimize the VoiceWave experience in Discord"):
            return True
        else:
            return False

    def close_title_2_alert_btn(self):
        """
        在title栏,点击第二个功能，弹出的一个弹窗，关闭此弹窗
        :return:
        """
        #
        control = self.main_window.GroupControl(ClassName='OptimizeTips', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=1)
        # 继承
        BasePage.click(self, control)

    def click_title_3_icon(self):
        """
        在title栏,点击设置菜单栏第3个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/3.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def click_title_4_icon(self):
        """
        在title栏,点击设置菜单栏第2个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/4.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def click_title_5_icon(self):
        """
        在title栏,点击设置菜单栏第2个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/5.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def click_title_6_icon(self):
        """
        在title栏,点击设置菜单栏第2个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/dis2.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def click_title_7_icon(self):
        """
        在title栏,点击设置菜单栏第2个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/7.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def close_title_7_alert_btn(self):
        """
        在title栏,点击第二个功能，弹出的一个弹窗，关闭此弹窗
        :return:
        """
        #
        control = self.main_window.GroupControl(ClassName='CUSerRateWnd', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=1)
        # 继承
        BasePage.click(self, control)

    def click_title_8_icon(self):
        """
        在title栏,点击设置菜单栏第2个
        :return:
        """
        global template_path
        try:
            # 拼接完整图片路径（字符串）
            template_path = "title/8.png"

            position = ScreenElement(project_root.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click()

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

    def click_title_9_icon(self):
        """
        在title栏,点击设置菜单栏第9个
        about弹窗页
        :return:
        """
        # 拼接完整图片路径（字符串）
        template_path = project_root.getImagePath("title/9.png")

        try:
            position = ScreenElement(template_path)
            # 找到该图标，点击操作
            position.click(delay=1)

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {template_path} 图标")
            raise TargetElementNotFoundError(f"未找到目标元素：{template_path}")

    def close_btn(self):
        """
        点击关闭按钮
        :return:
        """
        try:
            control = self.main_window.GroupControl(ClassName='AboutWidget', Depth=1).ButtonControl(
                ClassName='QPushButton', Depth=1)
            BasePage.click(self, control)
        except Exception as e:
            logger.error(f"{e}")
            logger.info("未找到关闭按钮")