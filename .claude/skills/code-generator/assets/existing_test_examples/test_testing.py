#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_testing.py
import allure
import pytest
import uiautomation as auto

from bases.basePage import logger
from commons.utils.targetNotFoundError import control_raise
from pom.voicewave_home_page import VoiceWavePage
from pom.voicewave_setting_page import VoicewaveSettingPage
from pom.voicewave_voice_creation_page import VoicewaveVoiceCreationPage


@allure.epic("PC 客户端")
@allure.feature("Testing")
class TestTesting:
    """
    Testing功能测试
    """
    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击扬声器下拉框-选择None")
    @pytest.mark.dependency(name="test_click_speaker")
    def test_click_speaker(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        setting = VoicewaveSettingPage(active_window)
        setting.allure_screenshot("进入Setting页面后")
        setting.click_speaker_combobox()
        setting.click_relative_to_element('nav6_settings/headphone.png', offset_x=0, offset_y=154)
        logger.info("====已通过相对位置点击扬声器下拉选项")
        setting.click_nav_list_item()
        setting.allure_screenshot("选择None后")
        notify = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='NotifiesManager', Depth=2).TextControl(
            Name='The headset or microphone is not set up correctly. Please go to reset it.', ClassName='QLabel', Depth=4)
        assert setting.find_control(notify), "未找到通知提示文本，测试失败"
        setting.allure_screenshot("通知提示出现后")
        logger.info("====已找到通知提示文本，测试通过")

    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击扬声器下拉框-选择正确设备-通知消失")
    @pytest.mark.dependency(depends=["test_click_speaker"])
    def test_speaker_select_device(self, active_window):
        setting = VoicewaveSettingPage(active_window)
        setting.click_nav_list_item()
        # 找到reset图片后相对鼠标位置偏移点击
        setting.find_element_and_click('nav6_settings/reset.png')
        setting.allure_screenshot("点击reset后")
        # 点击扬声器下拉框
        setting.click_speaker_combobox()
        # 通过图片相对位置点击
        setting.click_relative_to_element('nav6_settings/headphone.png', offset_x=0, offset_y=218)
        logger.info("====已通过相对位置点击扬声器下拉选项")
        # 点击导航栏ListItem
        setting.click_nav_list_item()
        # 验证reset图片不存在
        assert not setting.find_element('nav6_settings/reset.png'), "reset图片仍然存在，测试失败"
        setting.allure_screenshot("选择正确设备后")
        logger.info("====reset图片已消失，测试通过")

    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击麦克风下拉框-选择None")
    @pytest.mark.dependency(name="test_enter_setting")
    def test_enter_setting(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        setting = VoicewaveSettingPage(active_window)
        setting.allure_screenshot("进入Setting页面后")
        # 点击麦克风下拉框
        setting.click_microphone_combobox()
        # 鼠标移动到None选项
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ListItemControl(
            Name='None', foundIndex=1, Depth=9)
        if auto.WaitForExist(control, 5):
            nav.click(control)
            logger.info("====已点击麦克风None选项")
        else:
            logger.error("未找到麦克风None选项")
            assert False
        setting.allure_screenshot("选择None后")


    @allure.story("Setting页-General页")
    @allure.title("点击General页签后验证耳机选择标签存在")
    def test_general_headphone_label(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        setting = VoicewaveSettingPage(active_window)
        setting.allure_screenshot("进入Setting页面后")
        setting.click_setting_general_tab()
        setting.allure_screenshot("点击General Tab后")
        headphone_label = setting.find_headphone_label()
        control_raise(headphone_label, "General页未找到耳机选择标签", timeout=10)
        setting.allure_screenshot("找到耳机标签后")
        logger.info("====已找到耳机选择标签，用例成功")

    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击麦克风下拉框-选择正确设备-通知消失")
    @pytest.mark.dependency(depends=["test_enter_setting"])
    def test_microphone_select_device(self, active_window):
        setting = VoicewaveSettingPage(active_window)
        setting.click_nav_list_item()
        # 找到reset图片后点击
        setting.find_element_and_click('nav6_settings/reset.png')
        setting.allure_screenshot("点击reset后")
        # 点击麦克风下拉框
        setting.click_microphone_combobox()
        # 通过图片相对位置点击
        setting.click_relative_to_element('nav6_settings/microphone.png', offset_x=0, offset_y=218)
        logger.info("====已通过相对位置点击麦克风下拉选项")
        # 点击导航栏ListItem
        setting.click_nav_list_item()
        # 验证reset图片不存在
        assert not setting.find_element('nav6_settings/reset.png'), "reset图片仍然存在，测试失败"
        setting.allure_screenshot("选择正确设备后")
        logger.info("====reset图片已消失，测试通过")






