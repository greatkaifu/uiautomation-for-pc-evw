#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_title.py
import time

import allure
import pytest

from commons.utils.browser import Browser
from commons.utils.myLogging import get_logger
from pom.voicewave_home_page import VoiceWavePage
import uiautomation as auto

logger = get_logger()




@pytest.mark.usefixtures("window")
# @pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class TestTitle:
    """
    测试环境条件，程序处于未激活状态
    测试用例：
    1.测试标题
    """
    @allure.story("测试标题-编辑")
    def test_title_edit(self,window):
        """
        关闭程序的二次确认弹窗，点击OK确定按钮，关闭程序
        :return:
        """

        page=VoiceWavePage(window)
        page.click_title_edit()
        # 等待浏览器页面加载完成
        time.sleep(0.5)
        browser=Browser()
        assert browser.find_opened_url("https://docs.google.com/forms/d/e/1FAIpQLScvNPJobTEndjo6CjGX6ZXBsp_WsWJazIhdtmYDiSIxqt4KYA/viewform")== True
        browser.close_browser(strategy="window")

    @allure.story("测试标题-title栏的discord图标")
    def test_title_discord(self, window):
        page=VoiceWavePage(window)
        page.click_title_discord_icon()
        # 等待浏览器页面加载完成，在类里面已经增加等待方法
        browser=Browser()
        assert browser.find_opened_url("https://discord.com/invite/BV6WpX757q")== True
        browser.close_browser(strategy="window")
        try:
            # 关闭discord程序
            auto.PaneControl(Name='#rules📝 | VoiceWave - Discord', ClassName='Chrome_WidgetWin_1',
                             Depth=1).GroupControl(foundIndex=3, Depth=10).ButtonControl(Name='关闭', Depth=1).Click()
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到discord关闭按钮")

    @allure.story("测试标题-title栏的youtube图标")
    def test_title_youtube(self, window):
        page=VoiceWavePage(window)
        # 点击YouTube图标
        page.click_title_youtube_icon()
        # 等待浏览器页面加载完成
        browser=Browser()
        assert browser.find_opened_url("https://discord.com/invite/BV6WpX757q")== True
        browser.close_browser(strategy="window")
        try:
            # 关闭discord程序
            auto.PaneControl(Name='#rules📝 | VoiceWave - Discord', ClassName='Chrome_WidgetWin_1', Depth=1).GroupControl(foundIndex=3, Depth=10).ButtonControl(Name='关闭', Depth=1).Click()
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到discord关闭按钮")

    @allure.story("测试标题-title栏的最大化")
    def test_title_max(self, window):
        page = VoiceWavePage(window)
        # 点击最大化按钮
        page.click_title_max_icon()
        # 程序窗口最大化后，查找对应的图标
        assert page.find_title_max_icon() == True
        # 再次点击最大化按钮
        # 点击最大化按钮
        page.click_title_max_icon()
        # # 关闭程序
        # pro=CloseProgram(window)
        # # 关闭程序
        # pro.close_program()
        # # 选择退出方式
        # pro.select_exit_way()
        # # 二次确认弹窗点击OK按钮
        # pro.click_program_ok()

    @allure.story("测试标题-title栏的最小化")
    def test_title_min(self, window):
        page = VoiceWavePage(window)
        # 点击最大化按钮
        page.click_title_min_icon()
        # 程序窗口最大化后，查找对应的图标
        assert page.find_title_min_icon() == False
        # 再次点击最大化按钮
        # 点击最大化按钮
        window.SetActive()




    @allure.story("测试标题-title栏的设置菜单栏第1个功能")
    def test_title_setting_1(self, window):
        page = VoiceWavePage(window)
        # 点击最大化按钮
        page.click_title_setting_icon()
        # 程序窗口最大化后，查找对应的图标
        page.click_title_1_icon()
        browser = Browser()
        assert browser.find_opened_url("https://discord.com/invite/BV6WpX757q") == True
        browser.close_browser(strategy="window")
        try:
         # 关闭discord程序
         auto.PaneControl(Name='#rules📝 | VoiceWave - Discord', ClassName='Chrome_WidgetWin_1', Depth=1).GroupControl(foundIndex=3, Depth=10).ButtonControl(Name='关闭', Depth=1).Click()
        except Exception as e:
         logger.error(f"{e}")
         logger.error("未找到discord关闭按钮")



    @allure.story("测试标题-title栏的设置菜单栏第2个功能")
    def test_title_setting_2(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 查找对应的菜单栏的第2个功能
        page.click_title_2_icon()

        try:
            # 弹窗上的文本的控件地址
            control = window.GroupControl(ClassName='OptimizeTips', Depth=1).TextControl(
                Name='Optimize the VoiceWave experience in Discord', ClassName='QLabel', Depth=1)
            result=page.find_control(control,"Optimize the VoiceWave experience in Discord")
            assert result == True
            # 关闭discord弹窗
            page.close_title_2_alert_btn ()

        except Exception as e:
         logger.error(f"{e}")
         logger.error("未找到discord关闭按钮")


    @allure.story("测试标题-title栏的设置菜单栏第3个功能")
    def test_title_setting_3(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 程序窗口最大化后，查找对应的图标
        page.click_title_3_icon()
        browser = Browser()
        assert browser.find_opened_url("https://kb.easeus.com/other/90019.html") == True
        browser.close_browser(strategy="window")
    @allure.story("测试标题-title栏的设置菜单栏第4个功能")
    def test_title_setting_4(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 程序窗口最大化后，查找对应的图标
        page.click_title_4_icon()
        browser = Browser()
        assert browser.find_opened_url("https://www.youtube.com/@easeus_voicewave") == True
        browser.close_browser(strategy="window")

        # https://multimedia.easeus.com/support/voicewave/index.html

    @allure.story("测试标题-title栏的设置菜单栏第5个功能")
    def test_title_setting_5(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 程序窗口最大化后，查找对应的图标
        page.click_title_5_icon()
        browser = Browser()
        assert browser.find_opened_url("https://multimedia.easeus.com/support/voicewave/index.html") == True
        browser.close_browser(strategy="window")


    @allure.story("测试标题-title栏的设置菜单栏第6个功能")
    def test_title_setting_6(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 程序窗口最大化后，查找对应的图标
        page.click_title_6_icon()
        browser = Browser()
        assert browser.find_opened_url("https://secure.livechatinc.com/licence/1389892/v2/open_chat.cgi?groups=10") == True
        browser.close_browser(strategy="window")

    @allure.story("测试标题-title栏的设置菜单栏第7个功能")
    def test_title_setting_7(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 查找对应的菜单栏的第7个功能
        page.click_title_7_icon()

        try:
            # 弹窗上的文本的控件地址
            control = window.GroupControl(ClassName='CUSerRateWnd', Depth=1).TextControl(Name='Thank you for choosing EaseUS VoiceWave', ClassName='QLabel', Depth=2)
            result = page.find_control(control, 'Thank you for choosing EaseUS VoiceWave')
            assert result == True
            # 关闭discord弹窗
            page.close_title_7_alert_btn()

        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到feedback弹窗")



    @allure.story("测试标题-title栏的设置菜单栏第8个功能")
    def test_title_setting_8(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 查找对应的菜单栏的第8个功能
        page.click_title_8_icon()
        result = False
        try:
            # 弹窗上的文本的控件地址
            control = window.GroupControl(ClassName='updateNewWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
            # 如果弹窗上存在
            if page.find_control(control):
                # 点击控件
                page.click(control)
                result = True
            else:
                control = window.GroupControl(ClassName='CCheckUpdatePage', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
                page.click(control)
                result = True
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到更新弹窗")
        assert result == True

    @allure.story("测试标题-title栏的设置菜单栏第9个功能")
    def test_title_setting_9(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 查找对应的菜单栏的第9个功能
        page.click_title_9_icon()

        result = False
        try:
            # 弹窗上的文本的控件地址
            control = window.GroupControl(ClassName='AboutWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
            # 如果弹窗上存在
            if page.find_control(control):
                # 点击控件
                page.click(control)
                result = True
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到更新弹窗")
        assert result == True