#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : leikaifu
# @File    : voicewave_voice_creation_page$
# @Time    : 2026/3/24$ 21:12$
# @IDE     : PyCharm
from bases.basePage import logger, BasePage
from pom.voicewave_home_page import VoiceWavePage
import uiautomation

class VoicewaveVoiceCreationPage(VoiceWavePage):
    """
        克隆音效
    """

    def __int__(self, main_window):
        super().__init__(main_window)


    def click_clone_btn(self):
        """
        点击clone 按钮
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击clone sound按钮功能。")
                return True
            else:
                logger.error(f"未找到clone sound 按钮功能。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到clone sound 按钮功能。")
            return None
    def upload_video(self):
        """
        点击上传视频按钮
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).TextControl(ClassName='QLabel', Depth=10)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击上传视频按钮功能。")
                return True
            else:
                logger.error(f"未找到上传视频按钮功能。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到上传视频按钮功能。")
            return None



    def click_input(self):
        """
        点击 input输入框
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).EditControl(ClassName='QLineEdit', Depth=9)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击 input 输入框。")
                return True
            else:
                logger.error(f"未找到 input 输入框。")
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到 input 输入框。")
            return None
    def click_upload_voice(self):
        """
        点击 Click to upload voice files 控件
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(ClassName='QLabel', Depth=5)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击上传音频控件。")
                return True
            else:
                logger.error(f"未找到上传音频控件。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到上传音频控件。")
            return None

    def click_continue_btn(self):
        """
        点击 Continue 按钮
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(Name='Continue', ClassName='CustomBtn', Depth=4)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击 Continue 按钮。")
                return True
            else:
                logger.error(f"未找到 Continue 按钮。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到 Continue 按钮。")
            return None

    def click_back_btn(self):
        """
        点击 Back 按钮
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=7)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击 Back 按钮。")
                return True
            else:
                logger.error(f"未找到 Back 按钮。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到 Back 按钮。")
            return None

    def click_clone_submit_btn(self):
        """
            点击克隆提交按钮
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Clone Now', ClassName='CustomBtn', Depth=9)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info(f"已点击 clone 提交按钮。")
                return True
            else:
                logger.error(f"未找到 clone 提交按钮。")
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到 clone 提交按钮。")
            return None

























