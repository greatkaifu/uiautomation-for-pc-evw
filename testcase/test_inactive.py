#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_inactive.py.py
import time

import pytest

from commons.utils.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger
from pom.voicewave_discount_alert import DiscountAlert
from pom.voicewave_home_page import VoiceWavePage

logger = get_logger()

@pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class TestInactive:

    def test_active_alert_click_buy(self, main_window):
        """
        测试用例：实时变声器
        """
        # 创建对象
        page = VoiceWavePage(main_window)
        # 发现了启动折扣弹窗
        if page.find_start_alert():
            result=True
            # 关闭未激活新用户的启动弹窗
            page.close_start_alert_off()

        else:
            result=False

        assert result == True


    def test_title_active(self, main_window):
        """
        测试用例：激活 VoiceWave 主程序
        """
        # 实例化对象
        page = VoiceWavePage(main_window)
        # 触发title栏的upgrade按钮
        page.upgrade_click()
        result=page.find_is_active_alert()
        page.close_active_alert()

        assert result == True

    def test_nav1_active(self, main_window):
        """
        测试用例：导航列表1
        """
        page = VoiceWavePage(main_window)
        # 进入实时变声器
        page.nav1_realtime_voice_changer()
        #点击保存按钮，触发限制激活弹窗
        page.nav1_save_setting()
        # 判断弹窗是否出现
        result = page.find_is_active_alert()
        # 关闭弹窗
        page.close_active_alert()
        assert result == True

    def test_creation_active(self, main_window):
        """
        测试用例：克隆功能
        """
        # 实例化对象
        page = VoiceWavePage(main_window)
        # 进入克隆功能
        page.nav5_voice_creation()
        # 判断弹窗是否出现
        result = page.find_is_active_alert()
        # 关闭弹窗
        page.close_active_alert()
        assert result == True

    def test_per_ai_active(self, main_window):
        """
        测试用例：权限功能
        """
        # 创建对象
        alert = DiscountAlert(main_window)
        # 关闭未激活新用户的启动弹窗
        alert.close_newuser_start_alert()

        page = VoiceWavePage(main_window)

        # 进入实时变声器页
        page.nav1_realtime_voice_changer()

        project_root = GetPath()
        # 先找到滚动条
        find = ScreenElement(project_root.getImagePath("nav1_real_time_voice_changer/scroll.png"))
        if find.scroll_and_find():
            logger.info("找到滚动条")
            # 点击聚焦滚动条
            find.click()
        else:
            logger.error("未找到滚动条")
        # 任意查找一个AI音效，点击触发限制激活弹窗
        find=ScreenElement(project_root.getImagePath("nav1_real_time_voice_changer/active.png"))
        time.sleep(2)
        # 循环查找
        find.scroll_and_find()
        # 找到后触发点击
        find.click()
        # 判断弹窗是否出现
        result = page.find_is_active_alert()
        if result:
            logger.info("权限功能正常")
            # 关闭弹窗
            page.close_active_alert()
        assert result == True
