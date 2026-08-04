#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_testing.py
import allure
import pytest
import uiautomation as auto

from commons.utils.myLogging import get_logger
logger = get_logger()
from commons.utils.targetNotFoundError import control_raise
from pom.voicewave_home_page import VoiceWavePage
from pom.voicewave_setting_page import VoicewaveSettingPage


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
        logger.info("====已进入Setting页面")
        setting = VoicewaveSettingPage(active_window)
        setting.click_speaker_combobox()
        setting.click_relative_to_element('nav6_settings/headphone.png', offset_x=0, offset_y=154)
        logger.info("====已通过相对位置点击扬声器下拉选项")
        setting.click_nav_list_item()
        logger.info("====已点击导航栏ListItem")
        notify = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='NotifiesManager', Depth=2).TextControl(
            Name='The headset or microphone is not set up correctly. Please go to reset it.', ClassName='QLabel', Depth=4)
        assert setting.find_control(notify), "未找到通知提示文本，测试失败"
        logger.info("====已找到通知提示文本，测试通过")

    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击扬声器下拉框-选择正确设备-通知消失")
    @pytest.mark.dependency(depends=["test_click_speaker"])
    def test_speaker_select_device(self, active_window):
        setting = VoicewaveSettingPage(active_window)
        setting.click_nav_list_item()
        logger.info("====已点击导航栏ListItem")
        # 找到reset图片后相对鼠标位置偏移点击
        setting.find_element_and_click('nav6_settings/reset.png')
        logger.info("====已找到reset图片并相对鼠标位置点击")
        # 点击扬声器下拉框
        setting.click_speaker_combobox()
        # 通过图片相对位置点击
        setting.click_relative_to_element('nav6_settings/headphone.png', offset_x=0, offset_y=218)
        logger.info("====已通过相对位置点击扬声器下拉选项")
        # 点击导航栏ListItem
        setting.click_nav_list_item()
        logger.info("====已点击导航栏ListItem")
        # 验证reset图片不存在
        assert not setting.find_element('nav6_settings/reset.png'), "reset图片仍然存在，测试失败"
        logger.info("====reset图片已消失，测试通过")

    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击麦克风下拉框-选择None")
    @pytest.mark.dependency(name="test_enter_setting")
    def test_enter_setting(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        logger.info("====已进入Setting页面")
        # 点击麦克风下拉框
        setting = VoicewaveSettingPage(active_window)
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


    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击麦克风下拉框-选择正确设备-通知消失")
    @pytest.mark.dependency(depends=["test_enter_setting"])
    def test_microphone_select_device(self, active_window):
        setting = VoicewaveSettingPage(active_window)
        setting.click_nav_list_item()
        logger.info("====已点击导航栏ListItem")
        # 找到reset图片后点击
        setting.find_element_and_click('nav6_settings/reset.png')
        logger.info("====已找到reset图片并点击")
        # 点击麦克风下拉框
        setting.click_microphone_combobox()
        # 通过图片相对位置点击
        setting.click_relative_to_element('nav6_settings/microphone.png', offset_x=0, offset_y=218)
        logger.info("====已通过相对位置点击麦克风下拉选项")
        # 点击导航栏ListItem
        setting.click_nav_list_item()
        logger.info("====已点击导航栏ListItem")
        # 验证reset图片不存在
        assert not setting.find_element('nav6_settings/reset.png'), "reset图片仍然存在，测试失败"
        logger.info("====reset图片已消失，测试通过")

    @allure.story("Setting页")
    @allure.title("进入Setting页面-点击翻译Tab-滚轮查找multi_language_translation图片")
    def test_translate_text_scroll(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        logger.info("====已进入Setting页面")
        setting = VoicewaveSettingPage(active_window)
        # 点击翻译设置TabButton
        setting.click_translate_tab()
        logger.info("====已点击翻译TabButton")
        # 点击滚动区域获取焦点
        setting.click_translate_scroll_area()
        logger.info("====已点击滚动区域获取焦点")
        # 通过滚轮查找multi_language_translation图片
        result = setting.find_multi_language_translation_by_scroll()
        assert result == True, "未通过滚轮找到multi_language_translation图片，测试失败"
        logger.info("====已通过滚轮找到multi_language_translation图片，测试通过")

    @allure.story("Testing页")
    @allure.title("点击耳机TabButton-验证AI Calibration文本存在")
    @pytest.mark.test
    def test_click_headphone_tab(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        logger.info("====已进入Setting页面")
        setting = VoicewaveSettingPage(active_window)
        setting.click_headphone_tab()
        logger.info("====已点击耳机选择TabButton")
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).TextControl(
            Name='AI Calibration', ClassName='QLabel', Depth=7)
        control_raise(control, "AI Calibration文本")
        logger.info("====已找到AI Calibration文本，测试通过")


