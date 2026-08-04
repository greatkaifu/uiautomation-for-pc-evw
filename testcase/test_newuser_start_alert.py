#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_inactive.py.py
import subprocess
import time

import allure
import pytest

from commons.utils.configmanager import ConfigManager
from commons.utils.killProcess import kill_process_by_name

from pom.voicewave_closeprogram_page import CloseProgram
from pom.voicewave_discount_alert import DiscountAlert

@pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class TestNewUserAlert:
    """
    测试用例：
    新用户启动提示弹窗  只有一种启动模式
    新用户挽留弹窗 有三种弹窗模式 1、挽留弹窗   2、进入内购激活弹窗，点击关闭程序，挽留弹窗    3、进入内购激活弹窗并且点击buy now按钮，点击关闭程序，挽留弹窗
    老用户启动弹窗  只有一种启动模式
    老用户挽留弹窗 1.只有一种挽留弹窗模式
    """

    @pytest.mark.skip(reason="产品取消新用户启动弹窗")
    @allure.story("新用户启动弹窗")
    def test_newuser_start_alert(self,Inactive_main_window):
        """
        测试用例：新老用户启动弹窗每天只会弹一次
        """

        page = DiscountAlert(Inactive_main_window)
        text = page.find_newuser_start_alert()
        assert text == "Pro Bonus Bundle"
        # 弹窗已经发现，关闭启动弹窗
        page.close_newuser_start_alert()
        # 模拟关闭应用程序
        CloseProgram(Inactive_main_window).close_program()
        time.sleep(1)
        # 关闭程序，弹出挽留弹窗
        page.close_newuser_wait_alert_third()












