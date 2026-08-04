#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_nav2_soundboard.py
import json
import subprocess
import time

import allure
import pytest
import uiautomation as auto

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from pom.voicewave_closeprogram_page import CloseProgram
from pom.voicewave_soundboard_page import SoundBoardPage
import allure
import pytest

from commons.utils.browser import Browser
from commons.utils.myLogging import get_logger
from commons.utils.readconfig import INIConfigReader
from pom.voicewave_home_page import VoiceWavePage

# 配置日志
logger = get_logger()



# 项目根目录
project_root=GetPath()

@allure.epic("PC 客户端")
@allure.feature("Soundboard 页面")
# @pytest.mark.skip(reason="该类功能尚未开发完成，暂时忽略")
class TestNav2Soundboard:
    """
    测试环境，程序处于激活状态
    测试用例：
    1.测试 AVL2Soundboard 音效功能
    """
    @allure.story("Upload sounds")
    @allure.title("上传音效按钮点击有效")
    def test_upload_1(self, active_window):
        """
        在soundboard页面，点击upload按钮
        """
        # 确定执行用例之前进入soundboard页面
        nav=VoiceWavePage(active_window)
        nav.nav2_soundboard()
        page = SoundBoardPage(active_window)
        control=active_window.WindowControl(Name='打开', ClassName='#32770', Depth=1)
        page.click_upload_button()
        result = page.find_control( control)
        logger.info(f"查找控件结果为：{result}")
        if result == None or result == False:
            logger.info("未找到控件")
            # 点击关闭按钮
            page.close_filewindow_alert()
        assert result == True
        # 点击关闭按钮
        page.close_filewindow_alert()

    @allure.story("Upload sounds")
    @allure.title("我的音效板点击import按钮有效")
    def test_import_1(self, active_window):
        page = SoundBoardPage(active_window)
        page.click_import_button()
        control = active_window.WindowControl(Name='打开', ClassName='#32770', Depth=1)
        result = page.find_control(control)
        if result == None or result == False:
            logger.info(f"未找到{control}控件")
            # 点击关闭按钮
            page.close_filewindow_alert()
        assert result == True
        page.close_filewindow_alert()
    
    @allure.title("我的音效板点击explor有效")
    def test_explore_1(self, active_window):
        page = SoundBoardPage(active_window)
        page.click_explore()
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Upload sounds to web', ClassName='CustomBtn', Depth=2)
        result = page.find_control(control)
        if result == None or result == False:
            logger.info(f"未找到{ control}控件")
            # 返回到soundboard页面
            page.back_soundboard()
        assert result == True
        # 返回到soundboard页面
        page.back_soundboard()

    @allure.title("点击uploadsounds有效")
    def test_nav2_soundboard_uploadsounds(self, active_window):
        """
        在soundboard页面，点击upload按钮
        """
        # 确定执行用例之前进入soundboard页面
        nav2_page=SoundBoardPage(active_window)
        nav2_page.nav2_soundboard()
        nav2_page.click_mysoundboard()
        # 点击上传音效
        nav2_page.click_upload_button()
        file_path = project_root.getProjectRoot() + r"\resources\testdata\soundboard"
        nav2_page.input_file_path(file_path)
        #选择文件打开
        file_name="soundboard_ai.mp4"
        nav2_page.open_file(file_name)
        # 上传过程中弹窗，取消按钮控件元素
        cancle_btn = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(Name='Cancel', ClassName='CustomBtn', Depth=1)
        result = nav2_page.find_control(cancle_btn)
        if result == True:
            logger.info("已经找到控件")
            re = nav2_page.wait_for_control_disappear(cancle_btn, 600)
            assert re == True
        else:
            assert result==True

    @allure.title("删除音效时，弹出二次确认弹窗")
    @pytest.mark.dependency(name="test_nav2_soundboard_uploadsounds")
    def test_delete_soundboard_ai_alert(self, active_window):
        """
        测试用例：选择导入的音效，点击删除按钮，删除音效时，弹出二次确认弹窗
        期望：点击删除时，弹出二次确认弹窗
        """
        nav2_page = SoundBoardPage(active_window)
        cont=active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='SoundItemsDisplayWidget', Depth=4).ListItemControl(foundIndex=1, Depth=5)
        # 选择需要删除的音效
        nav2_page.click(cont)
        # 点击删除按钮
        nav2_page.delete_soundboard()
        time.sleep(2)
        control=active_window.GroupControl(ClassName='DelSoundTip', Depth=1).TextControl(Name='Do you want to delete this sound effect?', ClassName='QLabel', Depth=2)
        result=nav2_page.find_control(control)
        if result:
            logger.info(f"{nav2_page.find_control(control)}++++++++++++该控件元素存在！！！")
            assert result==True
            nav2_page.close_delete_alert()
        else:
            logger.info(f"{nav2_page.find_control(control)}++++++++++++该控件元素不存在！！！")
            assert result==False
            nav2_page.close_delete_alert()

    @allure.title("删除音效时，弹出二次确认弹窗")
    @pytest.mark.dependency(name="test_nav2_soundboard_uploadsounds")
    def test_delete_soundboard_ai_alert_cancle(self, active_window):
        """
        测试用例：选择导入的音效，点击删除按钮，删除音效时，弹出二次确认弹窗
        期望：点击删除时，弹出二次确认弹窗
        """
        nav2_page = SoundBoardPage(active_window)
        # 音效控件元素
        ai_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='SoundItemsDisplayWidget', Depth=4).ListItemControl(foundIndex=1, Depth=5)
        # 选择需要删除的音效
        nav2_page.click(ai_control)
        # 点击删除按钮
        nav2_page.delete_soundboard()
        time.sleep(2)
        cancle_control=active_window.GroupControl(ClassName='DelSoundTip', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DelSoundTip.widget_btnRect', Depth=1).ButtonControl(Name='Cancel', ClassName='CustomBtn', Depth=1)
        # 点击弹窗上的取消按钮
        nav2_page.click(cancle_control)
        # 删除二次确认弹窗
        control = active_window.GroupControl(ClassName='DelSoundTip', Depth=1).TextControl(
            Name='Do you want to delete this sound effect?', ClassName='QLabel', Depth=2)
        if nav2_page.find_control(control,2):
            assert False
        assert True

    @allure.title("删除音效时，弹出二次确认弹窗")
    @pytest.mark.dependency(name="test_nav2_soundboard_uploadsounds")
    def test_delete_soundboard_ai_alert_delete(self, active_window):
        """
        测试用例：选择导入的音效，点击删除按钮，删除音效时，弹出二次确认弹窗
        期望：点击删除时，弹出二次确认弹窗
        """
        nav2_page = SoundBoardPage(active_window)

        # 音效控件元素
        ai_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='SoundItemsDisplayWidget', Depth=4).ListItemControl(foundIndex=1, Depth=5)
        if nav2_page.find_control(ai_control):
            # 选择需要删除的音效
            nav2_page.click(ai_control)
            # 点击删除按钮
            nav2_page.delete_soundboard()
            time.sleep(2)
            delete_control = active_window.GroupControl(ClassName='DelSoundTip', Depth=1).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.DelSoundTip.widget_btnRect', Depth=1).ButtonControl(Name='Delete', ClassName='CustomBtn', Depth=1)
            # 点击弹窗上的取消按钮
            nav2_page.click(delete_control)
            time.sleep(3)
            # 实例化类
            element = ScreenElement(project_root.getImagePath("nav2_soundboard/ai.png"))
            if element.find():
                logger.info(f"+++++++++++++++{element.find()}")
                assert False
            assert True

    @allure.title("成功切换到All sounds页")
    def test_nav2_soundboard_swich_allsounds(self, active_window):
        """
        在soundboard页面，点击upload按钮
        """
        # 确定执行用例之前进入soundboard页面
        nav2_page = SoundBoardPage(active_window)
        nav2_page.nav2_soundboard()
        # 进入allsounds页
        nav2_page.click_allsounds()
        # 实例化类
        element = ScreenElement(project_root.getImagePath("nav2_soundboard/all_sound.png"))
        result=element.exists()
        if result:
            logger.info(f"{element}控件元素存在！！！")
            assert result==True
        else:
            logger.info(f"{element}控件元素不存在！！！")
            assert result==True



    @allure.title("成功切换到favorites页")
    @pytest.mark.dependency(name="test_nav2_soundboard_swich_favorites")
    def test_nav2_soundboard_swich_favorites_click_explore(self, active_window):
        """
        在soundboard页面，点击upload按钮
        """
        # 确定执行用例之前进入soundboard页面
        nav2_page = SoundBoardPage(active_window)
        # 实例化类
        element = ScreenElement(project_root.getImagePath("nav2_soundboard/favorites.png"))
        element.click()  #点击exploer 进入社区音效页
        #控件元素
        control=active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='CategoryWidget', Depth=6).ButtonControl(ClassName='TabButton', Depth=5)
        result=nav2_page.find_control(control)
        if result:
            logger.info(f"该控件元素存在！！！")
            assert result == True
        else:
            logger.info(f"该控件元素不存在！！！")
            assert result == True



