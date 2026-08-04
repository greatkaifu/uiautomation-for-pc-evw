#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_language.py


import time

import allure
import pytest
from rich import control

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.killProcess import kill_process_by_name
from commons.utils.languageSet import LanguageSet
from commons.utils.myLogging import get_logger
from pom.voicewave_closeprogram_page import CloseProgram
from pom.voicewave_discount_alert import DiscountAlert
from pom.voicewave_home_page import VoiceWavePage
from pom.voicewave_language_page import VoicewaveLanguagePage

# 配置日志
from pom.voicewave_login_page import UserLoginPage

import time
import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path


logger = get_logger()




class TestVoiceLanguage:
    """
    测试用例：
    1.测试 TestVoiceLanguage
    2.语言种类：

    ["English","French","German","Italian","Korean","Portuguese","Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"]

    """

    @allure.story('未激活新用户测试多语言 ["English","French","German","Italian","Korean","Portuguese","Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"]')
    def test_newuser_language(self, newuser_language_window):
        """
        测试多语言
        """

        # 测试用例
        # 解包元组
        main_window,lan =newuser_language_window
        # 窗口置顶处理
        main_window.SetTopmost( True)
        #多语言
        language=lan
        # 实例化截图对象
        p = VoicewaveLanguagePage(main_window)
        # 实例化 pom
        voicewave_page = VoiceWavePage(main_window)
        # 截图新用户--------启动弹窗多语言显示
        p.capture_picture(language)
        dis_alert_page=DiscountAlert(main_window)
        dis_alert_page.close_newuser_start_alert()

        # 未激活用户，第一类，未看见过激活弹窗价格页，点击关闭程序，弹出第一类挽留弹窗
        # 点击程序关闭按钮
        program = CloseProgram(main_window)
        program.close_program()
        # 截图退出程序，第一类挽留折扣弹窗
        p.capture_picture(language)
        dis_alert_page.close_newuser_wait_start_alert_first()
        # 关闭程序，弹出的二次确认弹窗
        p.capture_picture(language)
        program.close_exit_alert_btn()


        # 进入实时变声器
        voicewave_page.nav1_realtime_voice_changer()
        template_path = "language/nav1_1.png"
        p.click_ai(template_path)
        p.capture_picture(language)
        # 模式切换弹窗展示
        template_path = "language/nav1_2.png"
        p.click_ai(template_path)
        p.capture_picture(language)
        control_close_btn=main_window.GroupControl(ClassName='SwitchAiModelWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        voicewave_page.click(control_close_btn,timeout=5)
        #进入soundboard
        voicewave_page.nav2_soundboard()
        template_path = "language/nav2_1.png"
        p.click_ai(template_path)
        p.capture_picture(language)
        # 进入社区音效
        voicewave_page.nav3_community_library()
        template_path = "language/nav3_1.png"
        p.click_ai(template_path)
        p.capture_picture(language)
        # 进入文件变声器
        voicewave_page.nav4_file_voice_changer()
        p.capture_picture(language)
        # 进入克隆功能
        voicewave_page.nav5_voice_creation()
        p.capture_picture(language)
        # 进入设置功能
        voicewave_page.nav6_setting()
        p.capture_picture(language)
        # 进入快捷设置页
        control=main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='TabButton', foundIndex=2, Depth=6)
        voicewave_page.click(control,timeout=5)
        p.capture_picture(language)

        #进入设置按钮进入菜单栏
        voicewave_page.click_title_setting_icon()
        # 必须截取全屏图，才能查看多语言显示问题，设置菜单栏，已经超出程序界面
        p.capture_all_picture(language)

        # 查找对应的菜单栏的第9个功能，查看about页面
        voicewave_page.click_title_9_icon()
        p.capture_all_picture(language)
        voicewave_page.close_btn()


        # 第二类挽留弹窗，未激活新用户看了价格页，点击关闭程序，弹出第二类挽留弹窗
        # 进入限制激活弹窗页
        voicewave_page.upgrade_click()
        voicewave_page.close_active_alert()
        program.close_program()
        p.capture_picture(language)
        #通过图片处理， 分类
        template_path = "language/dis2.png"
        dis_alert_page.close_newuser_wait_alert_by_picture(template_path, -144, 217)
        program.close_exit_alert_btn()

        # 第三类挽留弹窗，未激活新用户看了价格页并且点击了buynow按钮，点击关闭程序，弹出第三类挽留弹窗
        voicewave_page.upgrade_click()
        # 截图激活限制弹窗
        p.capture_picture(language)
        time.sleep(3)

        voicewave_page.click_buy_now()
        # 激活程序窗口
        # language_window.SetActive(True)
        # language_window.SetFocus()
        time.sleep(3)
        p.capture_picture( language)
        #关闭提示登录弹窗
        control=main_window.GroupControl(ClassName='PurchaseStatusDialog', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        if control.Exists():
            voicewave_page.click(control,timeout=10)
        program.close_program()
        time.sleep(6)
        #截图操作
        p.capture_picture(language)
        # 通过图片处理，分类
        template_path = "language/dis3.png"
        dis_alert_page.close_newuser_wait_alert_by_picture(template_path, 263, 540)
        program.close_exit_alert_btn()
        assert main_window.Exists()

    @allure.story('未激活老用户测试多语言 ["English","French","German","Italian","Korean","Portuguese","Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"]')
    def test_olduser_language(self,olduser_language_window):
        """
        测试 用户登录相关多语言
        """

        # # 测试用例
        # 解包元组
        main_window, lan = olduser_language_window
        language = lan
        # 实例化截图对象
        p = VoicewaveLanguagePage(main_window)
        # 实例化 pom
        voicewave_page = VoiceWavePage(main_window)
        # 截图新用户--------启动弹窗多语言显示
        p.capture_picture(language)
        dis_alert_page = DiscountAlert(main_window)
        dis_alert_page.close_olduser_start_alert()
        # 激活
        # 进入限制激活弹窗页
        voicewave_page.upgrade_click()
        voicewave_page.close_active_alert()
        program = CloseProgram(main_window)
        program.close_program()
        dis_alert_page.close_olduser_Wait_alert()
        assert main_window.Exists()

    @allure.story('未激活老用户测试多语言 ["English","French","German","Italian","Korean","Portuguese","Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"]')
    def test_login_language(self, login_language_window):
        """
        测试
        """
        # 测试用例
        # 解包元组
        main_window, lan = login_language_window
        language = lan
        # 实例化截图对象
        capture = VoicewaveLanguagePage(main_window)
        # 折扣弹窗类
        dis_alert_page = DiscountAlert(main_window)
        # 实例化 pom
        voicewave_page = VoiceWavePage(main_window)
        #程序关闭类
        program = CloseProgram(main_window)
        # 登录页面类
        login_page = UserLoginPage(main_window)
        # 关闭启动折扣弹窗
        dis_alert_page.close_newuser_start_alert()
        # # 测试用例
        # # 进入设置按钮进入菜单栏
        # voicewave_page.click_title_setting_icon()
        # # 必须截取全屏图，查看用户在未登录状态时，login显示的多语言
        # capture.capture_all_picture(language)
        # # 第一条测试用例
        # #在title栏点击登录icon
        # login_page.click_login_icon()
        # #窗口激活状态,置顶
        # main_window.SetTopmost(True)
        # # 截图登录等待弹窗
        # capture.capture_picture(language)
        # time.sleep(2)
        # # 截图登录成功弹窗界面
        # capture.capture_picture(language)
        # # 第二条测试用例
        # # 进入用户登录页
        # time.sleep(6)
        # # 进入设置按钮进入菜单栏
        # voicewave_page.click_title_setting_icon()
        # # 必须截取全屏图，查看用户在未登录状态时，myacount显示的多语言
        # capture.capture_all_picture(language)
        # # 第三条测试用例
        # # 登录成功后
        # login_page.click_login_icon()
        # # 截图登录成功后，用户中心页面
        # capture.capture_picture(language)
        # # 查找元素位置
        # login1_path = "language/login1.png"
        # login_page.logout(login1_path, 627, 116)
        # # 退出账号二次确认弹窗截图
        # capture.capture_picture(language)
        # login2_path="language/login2.png"
        # login_page.logout_alert_ok(login2_path, -330, 221)
        #
        # # 测试先登录成功，关闭程序，断开网络，重启程序
        # # 登录成功后
        # login_page.click_login_icon()
        # kill_process_by_name("easeus.voicewave.exe")

        # 在title栏点击登录icon
        login_page.click_login_icon()
        time.sleep(5)
        capture.capture_picture(language)
        assert main_window.Exists()




        #
        # # 截图网络断开弹窗
        # capture.capture_picture(language)
        # # 在title栏点击登录icon
        # login_page.click_login_icon()
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)
        # #在title栏点击登录icon
        # login_page.click_login_icon()
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)
        # # 在title栏点击登录icon
        # login_page.click_login_icon()
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)
        # # 在title栏点击登录icon
        # login_page.click_login_icon()
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)
        # # 在title栏点击登录icon
        # login_page.click_login_icon()
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)
        # # 在title栏点击登录icon
        # login_page.click_login_icon()
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)

        #
        # # 在title栏点击登录icon
        # login_page.click_login_icon()
        # # main_window.GroupControl(ClassName='UserCenterWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1).Click()
        # position = ScreenElement(GetPath().getImagePath("language/login1.png"))
        # # 找到该图标，点击操作
        # if position.find():
        #     position.click_relative_to_element(offset_x=-188, offset_y=648)
        #
        # time.sleep(8)
        # capture.capture_picture(language)
        # login2_path = "language/login2.png"
        # login_page.close_btn(login2_path)
        #
    # @pytest.mark.test
    @allure.story('克隆页面多语言 ["English","French","German","Italian","Korean","Portuguese","Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"]')
    @allure.title("激活老用户进入克隆页面截图验证多语言显示")
    def test_creation_language(self, creation_language_window):
        """
        测试克隆页面多语言
        """
        # 解包元组
        main_window, lan = creation_language_window
        language = lan
        # 实例化截图对象
        capture = VoicewaveLanguagePage(main_window)
        # 实例化 pom
        voicewave_page = VoiceWavePage(main_window)
        project_root = GetPath()

        # 进入克隆功能
        voicewave_page.nav5_voice_creation()
        time.sleep(1)
        # 截图克隆页面
        capture.capture_picture(language)

        # 点击 CloneNowButton 控件
        clone_btn = main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='PreviewInfoWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.VoiceCreationWidget.stackedWidget.cloneWidget.AnimationStackedWidget.VoiceClonePreviewWidget.widget_info.PreviewInfoWidget', Depth=3).ButtonControl(ClassName='CloneNowButton', Depth=1)
        voicewave_page.click(clone_btn, timeout=5)
        # 截图
        capture.capture_picture(language)

        # 点击input图片打开文件管理器
        voicewave_page.find_element_and_click("多语言/input.png")
        # 输入文件路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
        voicewave_page.input_file_path(file_path)
        voicewave_page.open_file("5min.wav")
        time.sleep(1)
        # 再次截图
        capture.capture_picture(language)

        # 找到耳机图片，点击相对位置并截图
        voicewave_page.click_relative_to_element("多语言/耳机.png", 1530, 0)
        time.sleep(2)
        capture.capture_picture(language)


        # 找到Voice名称输入框控件并输入内容test123
        name_input = main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).GroupControl(ClassName='VoiceCloneWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.VoiceCreationWidget.stackedWidget.cloneWidget', Depth=1).CustomControl(ClassName='AnimationStackedWidget', Depth=1).GroupControl(ClassName='VoiceCloneCreateFormWidget', Depth=2).GroupControl(ClassName='QWidget', foundIndex=2, Depth=1).EditControl(ClassName='QLineEdit', Depth=1)
        voicewave_page.find_control_and_input(name_input, "test123")

        # 找到下拉按钮并点击，找到公开按钮相对位置64,-482并点击
        voicewave_page.find_element_and_click("多语言/下拉按钮.png")
        capture.capture_picture(language)
        voicewave_page.click_relative_to_element("多语言/公开按钮.png", 64, -482)

        # 找到耳机图片相对位置1043,-22并点击，等待一秒截图
        voicewave_page.click_relative_to_element("多语言/耳机.png", 1409,0)
        voicewave_page.click_relative_to_element("多语言/耳机.png", 1409,0)
        time.sleep(2)
        capture.capture_picture(language)

        close_btn = main_window.ButtonControl(ClassName='QPushButton', Depth=2)
        voicewave_page.wait_for_control_disappear(close_btn, timeout=120)
        # 找到默认头像图片相对位置0,12点击，截图，点击确定按钮图片
        voicewave_page.click_relative_to_element("多语言/头像.png", 0, 765)
        capture.capture_picture(language)

        # 找到关闭按钮图片相对位置-570,222点击
        voicewave_page.click_relative_to_element("多语言/关闭按钮.png", -570, 222)
        time.sleep(3)
        assert main_window.Exists()





















