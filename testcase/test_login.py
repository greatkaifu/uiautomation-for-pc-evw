#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_language.py


import time

import allure
import pytest

from commons.utils.browser import Browser
from commons.utils.myLogging import get_logger
from commons.utils.killProcess import kill_process_by_name
from pom.voicewave_closeprogram_page import CloseProgram
from pom.voicewave_discount_alert import DiscountAlert
from pom.voicewave_home_page import VoiceWavePage
from pom.voicewave_language_page import VoicewaveLanguagePage

from pom.voicewave_login_page import UserLoginPage
import pytest



# 配置日志
logger = get_logger()



@pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class TestVoiceLogin:
    """
    测试用例：
    1.测试 TestVoiceLogin

    """



    # @pytest.mark.test
    @allure.story("在title栏点击登录icon")
    def test_login(self, login_window):
        """
        测试
        """
        # 测试用例
        # 窗口
        main_window = login_window
        # 监听
        inspector = Browser(timeout=10)
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

        # 测试先登录成功，关闭程序，断开网络，重启程序
        # 登录成功后
        login_page.click_login_icon()
        time.sleep(2)
        inspector.get_current_browser_url()
        # 输出url地址信息
        url=inspector.get_current_browser_url()["url"]
        logger.info(url)
        assert "accounts.easeus.com" in url
        main_window.SetActive()
        # https://accounts.easeus.com/login


















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



















