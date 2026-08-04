#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_nav3_community.py
import time

import allure
import pyperclip
import pytest
import uiautomation as auto
from bases.basePage import logger
from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from pom.voicewave_community_page import VoicewaveCommunityPage

# @pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class  TestNav3Community:
    """
    社区音效功能
    """
    @allure.story("社区音效页，点击uploadsounds 按钮功能")
    def test_upload_sounds(self, active_window):
        """
        社区音效功能
        测试用例： 进入社区音效页，点击uploadsounds按钮，弹出弹窗
        期望：正常弹出弹窗
        """
        #实例化页面对象
        nav3_page=VoicewaveCommunityPage(active_window)
        # 进入社区音效功能页面
        nav3_page.nav3_community_library()
        nav3_page.click_uploadsounds_button()
        control=active_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).TextControl(Name='Upload sound to community', ClassName='QLabel', Depth=1)
        if nav3_page.find_control_text(control)=="Upload sound to community":
            assert  True
            logger.info("====点击uploadsounds按钮,弹窗正常弹出")
            nav3_page.close_uploadsounds_alert()
        else:
            logger.error("点击uploadsounds按钮,弹窗未正常弹出")
            assert False

    @allure.story("社区音效页，上传弹窗关闭按钮功能")
    def test_uploadsounds_close_btn(self, active_window):
        """
        社区音效功能
        测试用例： 进入社区音效页，点击uploadsounds按钮，点击关闭按钮
        期望：正常关闭弹窗
        """
        #实例化页面对象
        nav3_page=VoicewaveCommunityPage(active_window)
        # 进入社区音效功能页面
        nav3_page.click_uploadsounds_button()
        control=active_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        if nav3_page.find_control(control):
            nav3_page.click(control)
            assert  True
            logger.info("====点击uploadsounds按钮,弹窗正常关闭")
        else:
            logger.error("点击uploadsounds按钮,弹窗未正常关闭")
            assert False


    @allure.story("社区音效页，上传视频成功，sound name自动获取音频名称功能")
    @pytest.mark.parametrize("file_name", ["import_ai.mp4"])
    def test_upload_video_get_name(self, active_window,file_name):
        """
        社区音效功能
        测试用例： 进入社区音效页，选择音频上传成功,sounds name 名称自动获取音频默认的名称
        期望：sounds name 自动获取音频名称
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(active_window)
        # 首先进入社区音效功能页面
        nav3_page.nav3_community_library()
        # 在社区音效界面，点击uploadsounds 按钮
        nav3_page.click_uploadsounds_button()
        # 光标聚焦输入框
        nav3_page.click_input()
        # 已经聚焦输入框，全选输入框内容
        nav3_page.selectAll()
        # 清除输入框内容
        nav3_page.delete()
        # 删除按钮控制元素
        control = active_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=4)
        # 在打开弹窗时，如果开始上传有视频资源时，先删除此视频资源
        if nav3_page.find_control(control, timeout=1):
            nav3_page.click(control)
        nav3_page.upload_video(file_name)
        # 光标聚焦输入框
        nav3_page.click_input()
        # 已经聚焦输入框，全选输入框内容
        nav3_page.selectAll()
        nav3_page.copy()
        text = nav3_page.clip_output()
        if text==file_name.split( ".")[0]:
            logger.info("===sounds name 自动获取音频名称")
            # 关闭弹窗
            nav3_page.close_uploadsounds_alert()
            assert True
        else:
            # 关闭弹窗
            nav3_page.close_uploadsounds_alert()
            logger.error("===sounds name 未自动获取音频名称")
            assert False


    @allure.story("社区音效页，上传视频功能")
    @pytest.mark.parametrize("file_name", ["import_ai.mp4", "import_ai.m4a", "import_ai.mp3"])
    def test_upload_video(self, active_window, file_name):
        """
        社区音效功能
        测试用例： 进入社区音效页，选择音频上传成功 (150秒内的音频文件)
        期望：音频上传成功 ["import_ai.mp4", "import_ai.m4a", "import_ai.mp3"]
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(active_window)
        # 首先进入社区音效功能页面
        nav3_page.nav3_community_library()
        # 在社区音效界面，点击uploadsounds 按钮
        nav3_page.click_uploadsounds_button()
        control=active_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=4)
        # 在打开弹窗时，如果开始上传有视频资源时，先删除此视频资源
        if nav3_page.find_control(control):
            nav3_page.click(control)
        result=nav3_page.upload_video(file_name)
        if result:
            assert result == True
            nav3_page.close_uploadsounds_alert()
            logger.info("===上传成功")
        else:
            nav3_page.close_uploadsounds_alert()
            assert result == False
            logger.error("===上传失败")



    @allure.story("社区音效页，上传不同格式封面图")
    @pytest.mark.parametrize("image_name", ["image.jpeg","image.jpg","image.png","image_1.jpg"])
    def test_upload_image(self, active_window, image_name):
        """
        社区音效功能
        测试用例： 上传不同格式的封面图  ["image.jpeg","image.jpg","image.png","image_1.jpg"]
        期望：正常的上传
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(active_window)
        # 进入社区音效功能页面
        nav3_page.nav3_community_library()
        nav3_page.click_uploadsounds_button()
        result = nav3_page.upload_image(image_name)
        if result:
            assert result == True
            # 关闭弹窗
            nav3_page.close_uploadsounds_alert()
            logger.info("===上传成功")
        else:
            # 关闭弹窗
            nav3_page.close_uploadsounds_alert()
            assert result == False
            logger.error("===上传失败")
    @allure.story("社区音效页，上传弹窗sounds_name输入框输入音效名称功能")
    @pytest.mark.parametrize("sounds_name",["Caractères dans le champ de saisie", "入力ボックスの文字", "输入框的字符", "입력란의 문자"])
    def test_upload_image(self, active_window, sounds_name):
        """
        社区音效功能
        测试用例： 在上传弹窗，输入框输入音效名称
        期望：正常输入  ["Caractères dans le champ de saisie", "入力ボックスの文字", "输入框的字符", "입력란의 문자"]
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(active_window)
        # 进入社区音效功能页面
        nav3_page.nav3_community_library()
        nav3_page.click_uploadsounds_button()
        nav3_page.input_sounds_name(sounds_name)
        nav3_page.close_uploadsounds_alert()
        nav3_page.click_uploadsounds_button()
        # 光标聚焦输入框
        nav3_page.click_input()
        # 已经聚焦输入框，全选输入框内容
        nav3_page.selectAll()
        nav3_page.copy()

        text = nav3_page.clip_output()
        logger.info(f"===复制的文字为：{text}")
        if text==sounds_name:
            # 关闭弹窗
            nav3_page.close_uploadsounds_alert()
            logger.info("===输入音效名称成功！")
            assert True

        else:
            # 关闭弹窗
            nav3_page.close_uploadsounds_alert()
            logger.error("===输入音效名称失败！")
            assert False


    @allure.story("社区音效页，选择sound tag，缓存生效")
    @pytest.mark.parametrize("tag", ["memes", "games", "music", "anime", "sfx","comedians", "random", "politics", "movies"])
    def test_upload_close_alert_reopen(self, active_window,tag):
        """
        社区音效功能  ["memes", "games", "music", "anime", "sfx","comedians", "random", "politics", "movies", "sports", "other", "series", "youtube", "ttsong", "ttspeech", "2ttsong"]
        测试用例： 进入社区音效页，选择 sound tag，关闭弹窗，第二次打开成功保存上次选择记录
        期望：选择 sound tag 缓存生效
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(active_window)
        # 进入社区音效功能页面
        nav3_page.nav3_community_library()
        nav3_page.click_uploadsounds_button()
        nav3_page.select_tag(tag)
        nav3_page.close_uploadsounds_alert()
        nav3_page.click_uploadsounds_button()
        template_path = "nav3_community_library/" + tag + ".png"
        result = nav3_page.find_element(template_path)
        logger.info(f"===选择的tag为：{tag}")
        if result:
            nav3_page.close_uploadsounds_alert()
            assert True
            logger.info("===选择sound tag缓存生效")
        else:
            nav3_page.close_uploadsounds_alert()
            logger.error("===选择sound tag缓存失败")
            assert False

    @allure.story("社区音效页，提交上传sound功能")
    @pytest.mark.parametrize("param1,param2,param3,param4", [
        ("import_ai.m4a", "image.jpeg", "Caractères dans le champ de saisie", "memes"),
        ("import_ai.mp3", "image.png", "入力ボックスの文字", "games"),
        ("import_ai.mp4", "image.jpg", "입력란의 문자", "music")
    ])
    def test_upload_sound_submit(self,active_window,param1, param2, param3, param4):
        """
        社区音效功能
        测试用例： 提交上传的sound
        期望：提交成功
        """
        # 实例化页面对象
        nav3_page = VoicewaveCommunityPage(active_window)
        # 进入社区音效功能页面
        nav3_page.click_uploadsounds_button()
        nav3_page.upload_video(param1)
        nav3_page.upload_image(param2)
        nav3_page.input_sounds_name(param3)
        nav3_page.select_tag(param4)
        nav3_page.click_submit()
        # 成功提交控件元素
        control=active_window.GroupControl(ClassName='SBWebUploadDone', Depth=1).TextControl(Name='Upload Successful', ClassName='QLabel', Depth=1)
        result=nav3_page.wait_for_control_appear( control)
        # ok按钮控件元素
        control_ok=active_window.GroupControl(ClassName='SBWebUploadDone', Depth=1).ButtonControl(Name='OK', ClassName='CustomBtn', Depth=1)
        if result:
            nav3_page.click(control_ok)
            logger.info("===提交成功")
            assert True
        else:
            nav3_page.click(control_ok)
            logger.error("===提交失败")
            assert False
























