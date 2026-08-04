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
from commons.utils.readconfig import INIConfigReader
from pom.voicewave_home_page import VoiceWavePage

# 配置日志
logger = get_logger()




@pytest.mark.usefixtures("window")
# @pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class TestAbout:
    """
    测试用例：
    1.测试 about页面涉及的所有功能

    """
    @allure.story("测试标题-about页，跳转链接")
    def test_about_url(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 查找对应的菜单栏的第9个功能
        page.click_title_9_icon()
        # 点击链接，可以正常跳转
        control=window.GroupControl(ClassName='AboutWidget', Depth=1).TextControl(Name='https://multimedia.easeus.com/voice-changer/', ClassName='QLabel', Depth=1)
        page.click(control)
        browser = Browser()
        result=browser.find_opened_url("https://voicechanger.easeus.com/?testid=20260413&uid=S-1-5-21-4164000093-2963957314-936180009-1001&linkid=ad-evw-install&saSDKMultilink=true")
        logger.info(f"查找结果为：{result}")
        # 关闭已经打开的浏览器
        browser.close_browser()
        if result!= True:
            logger.info("未正常打开链接或打开URL地址和预期不符合！！！")
            page.close_btn()
        assert  result == True
        page.close_btn()





    @allure.story("测试标题-about页，点击关闭按钮正常关闭弹窗")
    def test_about_close_btn(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 找到对应的菜单栏的第9个功能
        page.click_title_9_icon()
        # 点击关闭按钮
        page.close_btn()
        control=window.GroupControl(ClassName='AboutWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        assert control.Exists() == False

    @allure.story("测试标题-about页，点击关闭按钮正常关闭弹窗")
    def test_about_close(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 找到对应的菜单栏的第9个功能
        page.click_title_9_icon()
        # 点击关闭按钮
        page.close_btn()
        control = window.GroupControl(ClassName='AboutWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        assert control.Exists() == False


    @allure.story("测试标题-about页，检查version是否正确")
    def test_about_version(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 找到对应的菜单栏的第9个功能
        page.click_title_9_icon()
        # 读取本地配置文件
        text = INIConfigReader().getconfig('about', 'version')
        logger.info(f"版本号：{text}")
        # version 控件元素位置
        control = window.GroupControl(ClassName='AboutWidget', Depth=1).TextControl(Name=text, ClassName='QLabel', Depth=1)

        result = page.find_control(control)
        logger.info(f"查找控件结果为：{result}")
        if result == None or result == False:
            logger.info("未找到控件")
            # 点击关闭按钮
            page.close_btn()
        assert result == True
        # 点击关闭按钮
        page.close_btn()

    @allure.story("测试标题-about页，检查激活状态")
    def test_about_active(self, window):

        page = VoiceWavePage(window)
        # 点击关闭按钮
        page.close_btn()

        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 找到对应的菜单栏的第9个功能
        page.click_title_9_icon()
        # 读取本地配置文件
        text = INIConfigReader().getconfig('about', 'active')
        # copyright 控件位置
        control = window.GroupControl(ClassName='AboutWidget', Depth=1).TextControl(Name=text, ClassName='QLabel', Depth=1)
        # 通过函数查找控件
        result=page.find_control(control)
        if result == None or result == False:
            logger.info("未找到控件")
            # 点击关闭按钮
            page.close_btn()
        assert result == True
        # 点击关闭按钮
        page.close_btn()
    @allure.story("测试标题-about页，检查copyright")
    def test_about_copyright(self, window):
        page = VoiceWavePage(window)
        # 点击设置按钮进入菜单栏
        page.click_title_setting_icon()
        # 找到对应的菜单栏的第9个功能
        page.click_title_9_icon()
        # 读取本地配置文件
        text = INIConfigReader().getconfig('about', 'copyright')
        # copyright 控件位置
        control = window.GroupControl(ClassName='AboutWidget', Depth=1).TextControl(Name=text, ClassName='QLabel', Depth=1)
        # 通过函数查找控件
        result = page.find_control(control)
        if result == None or result == False:
            logger.info("未找到控件")
            # 点击关闭按钮
            page.close_btn()
        assert result == True
        # 点击关闭按钮
        page.close_btn()