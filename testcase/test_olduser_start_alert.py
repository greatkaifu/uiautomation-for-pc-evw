#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_olduser_start_alert.py


import time

import allure
import pytest



from pom.voicewave_closeprogram_page import CloseProgram
from pom.voicewave_discount_alert import DiscountAlert


@pytest.mark.skip(reason="暂时不用执行")
class TestOldUserAlert:
    """
    测试用例：
    新用户启动提示弹窗  只有一种启动模式
    新用户挽留弹窗 有三种弹窗模式 1、挽留弹窗   2、进入内购激活弹窗，点击关闭程序，挽留弹窗    3、进入内购激活弹窗并且点击buy now按钮，点击关闭程序，挽留弹窗
    老用户启动弹窗  只有一种启动模式
    老用户挽留弹窗 1.只有一种挽留弹窗模式
    """

    @pytest.mark.skip(reason="产品取消老用户启动弹窗")
    @allure.story("老用户启动弹窗")
    def test_olduser_start_alert(self,old_main_window):
        """
        测试用例：未激活老用户激活弹窗
        """
        # 创建对象
        page = DiscountAlert(old_main_window)
        # 发现老用户的启动弹窗
        text= page.find_olduser_start_alert()
        assert text == "Claim Now"

        # 关闭启动弹窗
        page.close_olduser_start_alert()
        # # 模拟关闭应用程序
        CloseProgram(old_main_window).close_program()
        # 关闭挽留弹窗
        page.close_olduser_Wait_alert()

    @allure.story("老用户我挽留弹窗")
    def test_olduser_Wait_alert(self,old_main_window):
        """
        测试用例：未激活老用户挽留弹窗
        """
        page=DiscountAlert(old_main_window)
        # 关闭启动弹窗
        page.close_olduser_start_alert()
        # 关闭程序时候，触发挽留弹窗
        CloseProgram(old_main_window).close_program()
        # 判断挽留弹窗，是否正常出现
        text = page.find_olduser_Wait_alert()
        # 断言挽留弹窗是否正常显示
        assert text == "Limited Time Offer"
        # 关闭挽留弹窗
        page.close_olduser_Wait_alert()
