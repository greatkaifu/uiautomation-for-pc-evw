#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_community_page.py.py
import json
import time

from bases.basePage import logger, BasePage
from commons.utils.getProjectRroot import GetPath
from commons.utils.targetNotFoundError import control_raise
from pom.voicewave_home_page import VoiceWavePage
import uiautomation as auto


class VoicewaveCommunityPage(VoiceWavePage):
    """
    VoicewaveCommunityPage 主界面操作封装

    """
    def __int__(self, main_window):
        super().__init__(main_window)


    def click_uploadsounds_button(self):
        """
        在 community页，点击 uploadsounds 按钮（图片识别方式）
        """
        try:
            self.find_element_and_click("nav3_community_library/upload_button.png")
            logger.info(f"已点击uploadsounds 按钮功能。")
            return True
        except RuntimeError:
            logger.error(f"未找到uploadsounds 按钮功能。")
            return False
    def close_uploadsounds_alert(self):
        """
        在社区音效页，关闭uploadsounds弹窗
        """
        control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        control_raise(control, "community页-uploadsounds弹窗关闭按钮 ", timeout=10)
        BasePage.click(self, control)


    def click_input(self):
        """
        在社区音效页，点击进入输入框 input sounds name
        """
        basepage = BasePage(self.main_window)
        try:
            control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).GroupControl(ClassName='QWidget',
                                                                                                      AutomationId='FramelessWidget.SBWebUploadWidget.widget.widget_3',
                                                                                                      Depth=2).EditControl(
                ClassName='QLineEdit', Depth=1)
            control_raise(control, "community页-sounds name输入框 ", timeout=10)
            if basepage.find_control(control):
                basepage.click(control)
                return True
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到sounds name输入框。")
            return None

    def input_sounds_name(self,sounds_name):
        """
        在社区音效页，填写sounds name
        """
        basepage=BasePage(self.main_window)
        try:
            control=self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.SBWebUploadWidget.widget.widget_3', Depth=2).EditControl(ClassName='QLineEdit', Depth=1)
            control_raise(control, "community页-sounds name输入框 ", timeout=10)
            if basepage.find_control( control):
                basepage.click( control)
            # 已经聚焦输入框，全选输入框内容
            basepage.selectAll()
            # 删除全选内容
            basepage.delete()
            # 填写sounds name
            basepage.send_keys(sounds_name)
            logger.info(f"已填写sounds name。")
            return True
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到sounds name输入框。")
            return None

    def upload_video(self,file_name):
        """
        在社区音效页，上传sounds
        """
        try:
            nav3_page = VoicewaveCommunityPage(self.main_window)
            #删除按钮控制元素
            control_delete=self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=4)
            if nav3_page.find_control(control_delete, timeout=1):
                nav3_page.click(control_delete)
            # soundfile 控件元素
            control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).GroupControl(
                ClassName='SBWebSelFileWidget', Depth=3)
            if nav3_page.find_control(control):
                nav3_page.click(control)
                file_path = GetPath().getProjectRoot() + r"\resources\testdata\community\video"
                nav3_page.input_file_path(file_path)
                # 音频文件名称
                nav3_page.open_file(file_name)
                if nav3_page.wait_for_image_appear(GetPath().getImagePath("nav3_community_library/upload_1.png")):
                    logger.info("点击uploadsounds按钮,音频文件上传成功！！！")
                    return True
                else:
                    logger.error("点击uploadsounds按钮,音频文件上传成功！！！")
                    assert None
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"未找到上传video 按钮。")
            return None


    def upload_image(self,image_name):
        """
        在社区音效页，上传image
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(self.main_window)
        # upload image控件元素
        control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).GroupControl(ClassName='QWidget',
                                                                                                  AutomationId='FramelessWidget.SBWebUploadWidget.widget_5',
                                                                                                  Depth=1).ButtonControl(
            Name='Upload image', ClassName='CustomBtn', Depth=1)
        try :
            if nav3_page.find_control(control):
                nav3_page.click(control)
                file_path = GetPath().getProjectRoot() + r"\resources\testdata\community\picture"
                nav3_page.input_file_path(file_path)
                nav3_page.open_file(image_name)
                logger.info(f"图片已上传成功！！！")
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"{control}上传出异常！！！")
            return  None

    def select_tag(self, tag):
        """
        在社区音效页，选择tag
        """
        logger.info(f"开始选择tag:{tag}")
        # 实例化页面对象
        basepage = BasePage(self.main_window)
        basepage.find_element_and_click("nav3_community_library/upload_5.png")
        time.sleep(1)
        control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.SBWebUploadWidget.widget.widget_3', Depth=2).ListItemControl(Name=tag, Depth=3)
        control_raise(control, "community页-选择tag ", timeout=10)
        basepage.click(control)


    def click_submit(self):
        """
        在社区音效页，提交上传
        """
        logger.info(f"开始提交上传")
        control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(
            Name='Confirm', ClassName='CustomBtn', Depth=1)
        try:
            control_raise(control, "community页-提交上传按钮 ", timeout=10)
            self.click( control)
        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"{control}上传出异常！")
            return None





