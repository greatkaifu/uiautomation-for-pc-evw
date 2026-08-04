#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_left_navigation_bar.py
import allure
import pytest
import uiautomation as auto

from bases.basePage import logger
from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from pom.voicewave_home_page import VoiceWavePage


@allure.epic("PC 客户端")
@allure.feature("左侧导航栏")
class TestLeftNavigationBar:
    """
    左侧导航栏功能测试
    测试导航栏各菜单项点击切换是否正常
    """

    @allure.story("导航栏-实时变声")
    @allure.title("点击nav1实时变声菜单切换正常")
    def test_nav1_realtime_voice_changer(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav1_realtime_voice_changer()
        project_root = GetPath()
        position = ScreenElement(project_root.getImagePath("nav_bar/1.png"))
        if position.exists():
            logger.info("====nav1实时变声页面切换正常")
            assert True
        else:
            logger.error("nav1实时变声页面切换失败")
            assert False

    @allure.story("导航栏-Soundboard")
    @allure.title("点击nav2 Soundboard菜单切换正常")
    def test_nav2_soundboard(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav2_soundboard()
        project_root = GetPath()
        position = ScreenElement(project_root.getImagePath("nav_bar/2.png"))
        if position.exists():
            logger.info("====nav2 Soundboard页面切换正常")
            assert True
        else:
            logger.error("nav2 Soundboard页面切换失败")
            assert False

    @allure.story("导航栏-社区音效")
    @allure.title("点击nav3社区音效菜单切换正常")
    def test_nav3_community_library(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav3_community_library()
        project_root = GetPath()
        position = ScreenElement(project_root.getImagePath("nav_bar/3.png"))
        if position.exists():
            logger.info("====nav3社区音效页面切换正常")
            assert True
        else:
            logger.error("nav3社区音效页面切换失败")
            assert False

    @allure.story("导航栏-文件变声")
    @allure.title("点击nav4文件变声菜单切换正常")
    def test_nav4_file_voice_changer(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav4_file_voice_changer()
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='AnimationStackedWidget', Depth=1).GroupControl(
            ClassName='TabsWidget', foundIndex=1, Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(
            ClassName='TabButton', Depth=3)
        if auto.WaitForExist(control, 5):
            logger.info("====nav4文件变声页面切换正常")
            assert True
        else:
            logger.error("nav4文件变声页面切换失败")
            assert False


    @allure.story("导航栏-声音克隆")
    @allure.title("点击nav5声音克隆菜单切换正常")
    def test_nav5_voice_creation(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav5_voice_creation()
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).CustomControl(
            ClassName='AnimationStackedWidget', Depth=2).ButtonControl(
            ClassName='CloneNowButton', Depth=4)
        if auto.WaitForExist(control, 5):
            logger.info("====nav5声音克隆页面切换正常")
            assert True
        else:
            logger.error("nav5声音克隆页面切换失败")
            assert False

    @allure.story("导航栏-设置")
    @allure.title("点击nav6设置菜单切换正常")
    def test_nav6_setting(self, active_window):
        nav = VoiceWavePage(active_window)
        nav.nav6_setting()
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='TabsWidget', foundIndex=1, Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(
            ClassName='TabButton', Depth=3)
        if auto.WaitForExist(control, 5):
            logger.info("====nav6设置页面切换正常")
            assert True
        else:
            logger.error("nav6设置页面切换失败")
            assert False

