#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_soundboard_page.py


# 具体页面（业务封装）
import json
import time


import uiautomation as auto

from bases.basePage import BasePage
from bases.captureScreen import ScreenElement


# 配置日志
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import control_raise, element_raise
from pom.voicewave_home_page import VoiceWavePage


logger = get_logger()


class SoundBoardPage(VoiceWavePage):
    """EaseUS VoiceWave 主界面操作封装"""
    def __int__(self, main_window):
        super().__init__(main_window)

    @staticmethod
    def load_config():
        with open("test_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.info(f"===={config}")
        return config["test_values"]




    def click_upload_button(self):
        """
        在soundboard页，点击upload按钮

        """
        element_raise("nav2_soundboard/upload.png", "soundboard页面 upload按钮 ", timeout=10)
        self.find_element_and_click("nav2_soundboard/upload.png")

    def close_filewindow_alert(self):
        """
        获取导航列表
        文件管理器弹窗
        """
        control = self.main_window.TitleBarControl(Depth=2).ButtonControl(Name='关闭', Depth=1)
        control_raise(control, "文件管理器关闭按钮 ", timeout=10)
        BasePage.click(self, control)


    def click_import_button(self):
        """
        在soundboard页面，点击import按钮

        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='SoundItemsDisplayWidget', Depth=4).ListItemControl(Depth=5)
        control_raise(control, "soundboard页面 import按钮 ", timeout=10)
        BasePage.click(self, control)



    def click_explore(self):
        """
         在soundboard页面，点击 explore按钮

        """
        # 继承
        control=self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='SoundItemsDisplayWidget', Depth=4).ListItemControl(foundIndex=2, Depth=5)
        control_raise(control, "soundboard页面 explore按钮 ", timeout=10)
        BasePage.click(self, control)
        logger.info(f"已点击列表 explore功能。")

    def back_soundboard(self):
        """
         在soundboard页面，点击 back_soundboard按钮

        """
        # 继承
        control=self.main_window.ListControl(ClassName='CNaviListWidget', Depth=5).ListItemControl(foundIndex=2, Depth=1)
        control_raise(control, "soundboard页面 back_soundboard按钮 ", timeout=10)
        BasePage.click(self, control)


    def delete_soundboard(self):
        """
         在soundboard页面，点击 delet_soundboard按钮

        """
        # 继承
        control=self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.SoundLayoutWidget.widget_itemInfoCtl', Depth=2).GroupControl(ClassName='QScrollArea', Depth=4).ButtonControl(Name='Delete this sound', ClassName='CustomBtn', Depth=4)
        control_raise(control, "soundboard页面 delete按钮 ", timeout=10)
        BasePage.click(self, control)

    def alert_delete(self):
        """
         获取导航列表
         文件管理器弹窗
         """
        control = self.main_window.GroupControl(ClassName='DelSoundTip', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DelSoundTip.widget_btnRect', Depth=1).ButtonControl(Name='Delete', ClassName='CustomBtn', Depth=1)
        control_raise(control, "soundboard页面 delete按钮 ", timeout=10)
        BasePage.click(self, control)

    def alert_cancel(self):
        """
         获取导航列表
         文件管理器弹窗
         """
        control = self.main_window.GroupControl(ClassName='DelSoundTip', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DelSoundTip.widget_btnRect', Depth=1).ButtonControl(Name='Cancel', ClassName='CustomBtn', Depth=1)
        control_raise(control, "soundboard页面 cancel按钮 ", timeout=10)
        BasePage.click(self, control)

    def alert_close(self):
        """
         获取导航列表
         文件管理器弹窗
         """
        control = self.main_window.GroupControl(ClassName='DelSoundTip', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        control_raise(control, "soundboard页面 关闭二次确认弹窗按钮 ", timeout=10)
        BasePage.click(self, control)

    def close_delete_alert(self):
        """
        删除音效时，弹出二次确认弹窗
        关闭二次确认弹窗
        """
        control=self.main_window.GroupControl(ClassName='DelSoundTip', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        control_raise(control, "soundboard页面 关闭二次确认弹窗按钮 ", timeout=10)
        BasePage.click(self, control)


    def click_allsounds(self):
        """
        进入allsounds页面

        """
        element_raise("nav2_soundboard/my_sounds.png", "soundboard页面 allsounds按钮 ", timeout=10)
        self.find_element_and_click("nav2_soundboard/my_sounds.png")

    def click_favorites(self):
        """
        进入favorites页面

        """
        control=self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='CategoryWidget', Depth=6).ButtonControl(ClassName='TabButton', foundIndex=2, Depth=5)
        control_raise(control, "soundboard页面 favorites按钮 ", timeout=10)
        BasePage.click(self, control)


    def click_mysoundboard(self):
        """
        进入在soundboard页面，点击 mysounds按钮
        点击mysounds，进入mysounds页面
        """
        control=self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='CategoryWidget', Depth=6).ButtonControl(ClassName='TabButton', foundIndex=3, Depth=5)
        control_raise(control, "soundboard页面 mysounds按钮 ", timeout=10)
        BasePage.click(self, control)
