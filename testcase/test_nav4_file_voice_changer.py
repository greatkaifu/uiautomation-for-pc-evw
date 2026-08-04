#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : test_nav4_file_voice_changer.py
import os
import time
from pathlib import Path
import allure
import pytest
import uiautomation
import uiautomation as auto
from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger
from commons.utils.readconfig import INIConfigReader
from commons.utils.targetNotFoundError import control_raise
from pom.voicewave_file_voicechanger_page import FileVoiceChangerPage

# 配置日志
logger = get_logger()
# 实例化获取项目路径类
project_root = GetPath()


class TestNav4FileVoiceChanger:
    """
    测试环境条件，程序处于激活状态
    测试用例：
    1.测试 AVL4FileVoiceChanger 音效功能
    """
    @allure.story("上传音效按钮点击有效")
    def test_import_vaild(self, active_window):
        """
        在soundboard页面，点击upload按钮
        """
        nav4_page = FileVoiceChangerPage(active_window)
        nav4_page.filemanager_alert()

        # 在文件模式页，点击import按钮，进入文件管理器页
        control = active_window.ButtonControl(Name='取消', ClassName='Button', Depth=2)
        # 通过函数查找控件
        result = nav4_page.find_control(control)
        if result == False:
            logger.info("未找到控件")
            # 关闭文件管理器页
            nav4_page.close_filemanager()
        assert result == True
        # 关闭文件管理器页
        nav4_page.close_filemanager()

    @allure.story("正常关闭文件管理器页")
    def test_filemanager_close(self, active_window):
        """
        在soundboard页面，点击upload按钮
        """
        # 确定执行用例之前进入soundboard页面
        nav4_page = FileVoiceChangerPage(active_window)
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.filemanager_alert()
        # 文件管理器页的关闭按钮元素
        control = active_window.TitleBarControl(Depth=2).ButtonControl(Name='关闭', Depth=1)
        # 通过函数查找控件
        result = nav4_page.find_control(control)
        if result == False:
            logger.info("未找到控件")
            assert result == False
            # 关闭文件管理器页
            nav4_page.close_filemanager()
        # 关闭文件管理器页
        nav4_page.close_filemanager()

    @allure.story("上传 wmv 格式文件")
    @pytest.mark.parametrize("format_name", ["wav", "mp3", "mp4", "wmv", "m4a"])
    def test_import_wmv(self, active_window, format_name):
        """
        在nav4_page页面，上传 wmv 格式文件  ["ac3","wav", "mp3", "aac", "mp4", "wmv", "m4a", "mp2"]

        """
        # 确定执行用例之前进入soundboard页面
        nav4_page = FileVoiceChangerPage(active_window)
        # 导入支持格式文件的路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "sample." + format_name
        nav4_page.open_file(filename)
        # 文件已经到成功状态页面的back按钮元素
        control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back',
                                                                                                 ClassName='CustomBtn',
                                                                                                 Depth=3)
        result = nav4_page.find_control(control)
        if result == True:
            logger.info("已经找到控件")
            assert result == True
            # 返回import页
            nav4_page.back_btn_click()
        assert result == True
        # 返回import页
        nav4_page.back_btn_click()

    @allure.story("点击重新选择文件按钮，重新导入文件")
    def test_reselect_file(self, active_window):
        """
         在nav4_page页面，重新选择文件
         测试用例：点击 reselectfile
         期望：重新导入文件成功
        """
        # 确定执行用例之前进入soundboard页面
        nav4_page = FileVoiceChangerPage(active_window)
        # 导入支持格式文件的路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "sample.mp4"
        nav4_page.open_file(filename)

        # 点击reselectfile 按钮元素
        reselect_file = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', Depth=4).ButtonControl(Name='Reselect file', ClassName='CustomBtn', Depth=1)
        logger.info("已经找到控件")
        # 点击重新选择文件按钮
        nav4_page.click(reselect_file)
        # 导入支持格式文件路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "sample.mp4"
        nav4_page.open_file(filename)
        # 上传过程中弹窗，取消按钮控件元素
        cancle_btn = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(Name='Cancel', ClassName='CustomBtn', Depth=1)
        result = nav4_page.find_control(cancle_btn)
        if nav4_page.find_control(cancle_btn) == True:
            logger.info("已经找到控件")  # 重新导入成功
            re=nav4_page.wait_element_disappear(cancle_btn, 60)
            assert re == True
            # 返回import页
            nav4_page.back_btn_click()
        assert result == True
        # 返回import页
        nav4_page.back_btn_click()






    @allure.story("在上传过程中，点击弹窗上的取消功能")
    def test_import_alert_cancel(self, active_window):
        """
         在nav4_page页面，在上传过程中，点击弹窗上的取消功能
        """
        nav4_page = FileVoiceChangerPage(active_window)
        # 导入支持格式文件的路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "importcancel.mp4"
        nav4_page.open_file(filename)
        # 文件已经到成功状态页面的back按钮元素
        control = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(Name='Cancel',
                                                                                                     ClassName='CustomBtn',
                                                                                                     Depth=1)

        if nav4_page.find_control(control) == True:
            logger.info("已经找到控件")
            time.sleep(6)
            # 点击文件管理器弹窗页的关闭按钮
            nav4_page.click(control)
            control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
                ClassName='QWidget', Depth=3).TextControl(Name='Click to import the audio/video file',
                                                          ClassName='QLabel', Depth=3)
            reslut = nav4_page.find_control(control, timeout=10)
            assert reslut == True
        else:
            logger.info("没有打开文件管理器弹窗")
            assert False

    @allure.story("在上传过程中，点击弹窗上的关闭功能")
    def test_import_alert_close(self, active_window):
        """
         在nav4_page页面，在上传过程中，点击弹窗上的关闭功能
        """
        nav4_page = FileVoiceChangerPage(active_window)
        # 导入支持格式文件的路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"

        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "importcancel.mp4"
        nav4_page.open_file(filename)
        # 文件已经到成功状态页面的back按钮元素
        control = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(
            ClassName='QPushButton', Depth=1)
        if nav4_page.find_control(control) == True:
            logger.info("已经找到控件")
            time.sleep(6)
            # 点击文件管理器弹窗页的关闭按钮
            nav4_page.click(control)
            control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
                ClassName='QWidget', Depth=3).TextControl(Name='Click to import the audio/video file',
                                                          ClassName='QLabel', Depth=3)
            reslut = nav4_page.find_control(control, timeout=10)
            assert reslut == True
        else:
            logger.info("没有打开文件管理器弹窗")
            assert False

    @allure.story("在上传路径地址，法语")
    @pytest.mark.parametrize("dir_value",
                             ["Caractères dans le champ de saisie", "الأحرف في حقل الإدخال", "入力ボックスの文字", "输入框的字符",
                              "입력란의 문자"])
    def test_import_path_language(self, active_window, dir_value):
        """
         在nav4_page页面，在上传过程中路径地址，法语  Caractères dans le champ de saisie
        """
        nav4_page = FileVoiceChangerPage(active_window)
        # 导入支持格式文件的路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\导入多语言路径" + "\\" + dir_value
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "test.mp4"
        nav4_page.open_file(filename)
        # 文件已经到成功状态页面的back按钮元素
        control_back = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back',
                                                                                                      ClassName='CustomBtn',
                                                                                                      Depth=3)
        if nav4_page.find_control(control_back) == True:
            logger.info("已经找到控件")
            reslut = nav4_page.find_control(control_back, timeout=10)
            assert reslut == True
            control_back = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back',
                                                                                                          ClassName='CustomBtn',
                                                                                                          Depth=3)
            nav4_page.click(control_back)
        else:
            logger.info("没有打开文件管理器弹窗")
            assert False
    @allure.story("在导出路径地址，Caractères dans le champ de saisie ,الأحرف في حقل الإدخال,入力ボックスの文字,输入框的字符,입력란의 문자")
    @pytest.mark.parametrize("dir_value",  ["Caractères dans le champ de saisie", "الأحرف في حقل الإدخال", "入力ボックスの文字", "输入框的字符","입력란의 문자"])
    def test_output_path_language(self, active_window, dir_value):
        """
         在nav4_page页面，在上传过程中路径地址
         测试用例：支持多语言地址正常导出
         期望：在多语言路径地址正常导出

        ["Caractères dans le champ de saisie", "الأحرف في حقل الإدخال", "入力ボックスの文字", "输入框的字符","입력란의 문자"]

        """
        nav4_page = FileVoiceChangerPage(active_window)
        # back按钮控件元素地址
        back_btn=active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=3)
        if nav4_page.find_control(back_btn,timeout=2):
            nav4_page.back_btn_click()
        # 导入多语言路径
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"

        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "sample.mp4"
        nav4_page.open_file(filename)
        if not nav4_page.find_export():
            # 导出路径地址
            assert False
        # 导出多语言路径
        file_path = project_root.getProjectRoot() + r"\resources\testdata\导出多语言路径" + "\\" + dir_value
        nav4_page.check_output_path(file_path)
        # 点击导出按钮
        nav4_page.export_click()
        # 导入完成弹窗上的关闭按钮元素
        export_succeeded = active_window.GroupControl(ClassName='ExportWidget', Depth=1).TextControl(Name='Export succeeded!', ClassName='QLabel', Depth=3)
        # 查找控件元素是否存在
        result = nav4_page.find_control(export_succeeded, timeout=2)
        if not result:
            logger.info("未查找到导出成功的提示弹窗")
            assert False
        # 关闭导出成功弹窗
        nav4_page.close_export_succeeded_alert()
        # 后置清空输出目录
        nav4_page.clear_directory(file_path)
        assert result == True

    @allure.story("导入视频无音频流文件，弹出提示导入失败弹窗")
    def test_import_file_failed1(self, active_window):
        """
         用例：导入视频无音频流的文件，弹出导入失败提示弹窗
         预期：导入视频无音频流文件弹出提示失败弹窗
        """
        nav4_page = FileVoiceChangerPage(active_window)
        # back按钮元素地址
        back_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=3)
        # 如果back按钮元素存在，则点击back按钮，回到导入文件模式页
        if nav4_page.find_control(back_btn, timeout=1) == True:
            nav4_page.click(back_btn, timeout=1)
        # 路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "无音频轨道的视频.mp4"
        nav4_page.open_file(filename)
        control_text = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).TextControl(
            Name='Import failed. Please try again.', ClassName='QLabel', Depth=3)
        if nav4_page.find_control_text(control_text) == 'Import failed. Please try again.':
            logger.info("已经找到导入失败提示弹窗")
            # 导入文件失败，弹出失败提示弹窗，关闭失败提示弹窗
            nav4_page.close_import_failed_alert()
            assert True
        else:
            logger.info("没有找到导入失败提示弹窗")
            assert False


    @allure.story("导入视频无音频流文件，弹出失败提示弹窗，点击OK按钮，提示弹窗正常关闭")
    def test_import_file_failed2(self, active_window):
        """
         用例：导入视频无音频流的文件，弹出导入失败提示弹窗，点击OK按钮
         预期：点击OK按钮，弹窗正常关闭。
        """
        nav4_page = FileVoiceChangerPage(active_window)
        #back按钮元素地址
        back_btn= active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=3)
        # 如果back按钮元素存在，则点击back按钮，回到导入文件模式页
        if nav4_page.find_control(back_btn, timeout=1) == True:
            nav4_page.click(back_btn, timeout=1)
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "无音频轨道的视频.mp4"
        nav4_page.open_file(filename)
        control_text = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).TextControl(
            Name='Import failed. Please try again.', ClassName='QLabel', Depth=3)
        if nav4_page.find_control_text(control_text) == 'Import failed. Please try again.':
            logger.info("已经找到导入失败提示弹窗")
            # 导入文件失败，弹出失败提示弹窗，关闭失败提示弹窗
            nav4_page.import_failed_alert_click_ok()
            assert True
        else:
            logger.info("没有找到导入失败提示弹窗")
            assert False

    @allure.story("导入视频无音频流文件，弹出失败提示弹窗，点击关闭按钮，提示弹窗正常关闭")
    def test_import_file_failed3(self, active_window):
        """
         用例：导入视频无音频流的文件，弹出导入失败提示弹窗，点击关闭按钮
         预期：点击弹窗关闭按钮，弹窗正常关闭。
        """
        nav4_page = FileVoiceChangerPage(active_window)
        #back按钮元素地址
        back_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=3)
        # 如果back按钮元素存在，则点击back按钮，回到导入文件模式页
        if nav4_page.find_control(back_btn, timeout=1) == True:
            nav4_page.click(back_btn, timeout=1)
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "无音频轨道的视频.mp4"
        nav4_page.open_file(filename)
        control_text = active_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).TextControl(
            Name='Import failed. Please try again.', ClassName='QLabel', Depth=3)
        if nav4_page.find_control_text(control_text) == 'Import failed. Please try again.':
            logger.info("已经找到导入失败提示弹窗")
            # 导入文件失败，弹出失败提示弹窗，关闭失败提示弹窗
            nav4_page.close_import_failed_alert()
            assert True
        else:
            logger.info("没有找到导入失败提示弹窗")
            assert False

    @allure.story("导入视频无音频流文件，弹出失败提示弹窗，点击关闭按钮，提示弹窗正常关闭")
    @pytest.mark.parametrize("format_name",
                             ['MP3', 'M4A'])
    def test_convert_format(self, active_window, format_name):
        """
         用例：导入一种格式视频，导出转换成各种格式
         预期：成功的转换成 ['MP3','M4A','WAV','WMA','OGG','FLAC','MP4','MKV','AVI','FLV','MOV']
        """
        nav4_page = FileVoiceChangerPage(active_window)
        # back按钮控件地址
        back_btn=active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=3)
        if nav4_page.find_control(back_btn, timeout=2):
            nav4_page.back_btn_click()
        # 导入音视频资源
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"
        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)

        filename = "soundboard_ai.mp4"
        nav4_page.open_file(filename)

        if not nav4_page.find_export():
            # 导出路径地址
            logger.info("没有找到导出按钮")
        # 输出格式文件路径地址
        file_path = project_root.getProjectRoot() + r"\resources\testdata\输出格式文件" + "\\" + format_name
        # 前置清空输出目录
        nav4_page.clear_directory(file_path)
        # 如果路径不存在则创建，存在则忽略
        os.makedirs(file_path, exist_ok=True)
        nav4_page.check_output_path(file_path)
        # 选择需要转换的格式
        nav4_page.file_convert_to_format(format_name)
        # 点击导出按钮
        nav4_page.export_click()
        #导出成功后提示弹窗上的关闭按钮元素
        close_btn = active_window.GroupControl(ClassName='ExportWidget', Depth=1).ButtonControl(ClassName='QPushButton',
                                                                                                Depth=1)
        if not nav4_page.find_control(close_btn, timeout=10):
            logger.info("已经找到导出过程弹窗上的关闭按钮控件")
            assert False
        nav4_page.click(close_btn, timeout=10)
        file_style = "." + format_name
        logger.info(f"正在检查文件格式为：{file_style}")
        result = nav4_page.check_flie_and_delete(file_path, file_style)
        assert result == True

    @allure.story("音视频转换成功弹出提示弹窗，点击OK按钮，提示弹窗正常关闭")
    @pytest.mark.dependency(name="test_output_path_language")
    def test_convert_format_successed_alert_ok(self, active_window):
        """
         用例：音视频转换成功弹出提示弹窗
         预期：点击提示弹窗的OK按钮，弹窗消失
        """
        nav4_page = FileVoiceChangerPage(active_window)
        # 点击导出按钮
        nav4_page.export_click()
        ok_btn=active_window.GroupControl(ClassName='ExportWidget', Depth=1).ButtonControl(Name='OK', ClassName='CustomBtn', Depth=3)
        if nav4_page.export_succeeded_appear():
            logger.info("已经找到音视频转换成功提示弹窗")
            # 导出成功，点击弹窗上的OK按钮，弹窗正常关闭
            nav4_page.click(ok_btn, timeout=1)
            if not nav4_page.export_succeeded_appear():
                logger.info("未找到音视频转换成功提示弹窗")
                assert True
            else:
                logger.info("找到音视频转换成功提示弹窗,说明点击OK按钮，没有正常关闭")
                assert False
    @allure.story("超链接按钮测试")
    @allure.title("音视频转换成功弹出提示弹窗，点击超链接，打开文件资源管理器")
    def test_convert_format_successed_alert_link(self, active_window):
        """
         用例：音视频转换成功弹出提示弹窗
         预期：点击提示弹窗的Open按钮，弹窗正常关闭
        """
        #
        nav4_page = FileVoiceChangerPage(active_window)
        # back按钮控件元素地址
        back_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back',
                                                                                                  ClassName='CustomBtn',
                                                                                                  Depth=3)
        if nav4_page.find_control(back_btn, timeout=2):
            # 如果存在back按钮，则点击回到非实时变音模式页
            nav4_page.back_btn_click()
        # 导入多语言路径
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"

        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "import.mp4"
        nav4_page.open_file(filename)
        if not nav4_page.find_export():
            # 导出路径地址
            assert False
        # 导出多语言路径
        file_path = project_root.getProjectRoot() + r"\resources\testdata\导出多语言路径" + "\\" + "点击超链"
        # 切换导出路径
        nav4_page.check_output_path(file_path)
        # 点击导出按钮
        nav4_page.export_click()
        template_path= "nav4_file_voice_changer/success.png"
        element= ScreenElement(GetPath().getImagePath(template_path))
        if not nav4_page.export_succeeded_appear():
           logger.info("未找到音视频转换成功提示弹窗")
           assert  False
        element.click_relative_to_element(offset_x=200, offset_y=265)
        logger.info("已经找到音视频转换成功提示弹窗")
        # 关闭，点击超链弹出的文件资源管理器
        element1 = ScreenElement(GetPath().getImagePath("nav4_file_voice_changer/link.png"))
        time.sleep(3)
        if element1.exists():
            logger.info("已经打开文件资源管理器")
            assert  True
        else:
            logger.info("未打开文件资源管理器")
            assert False

    @allure.story("超链接按钮测试")
    @allure.title("音视频转换成功弹出提示弹窗，点击超链接，打开文件资源管理器")
    def test_convert_format_successed_alert_openfolder(self, active_window):
        """
         用例：音视频转换成功弹出提示弹窗
         预期：点击提示弹窗的Open按钮，弹窗正常关闭
        """
        #
        nav4_page = FileVoiceChangerPage(active_window)
        # back按钮控件元素地址
        back_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back',
                                                                                                  ClassName='CustomBtn',
                                                                                                  Depth=3)
        if nav4_page.find_control(back_btn, timeout=2):
            # 如果存在back按钮，则点击回到非实时变音模式页
            nav4_page.back_btn_click()
        # 导入多语言路径
        file_path = project_root.getProjectRoot() + r"\resources\testdata\支持格式文件"

        # 在文件模式页，点击import按钮，进入文件管理器页
        nav4_page.import_btn_filemanager(file_path)
        filename = "import.mp4"
        nav4_page.open_file(filename)
        if not nav4_page.find_export():
            # 导出路径地址
            assert False
        # 导出多语言路径
        file_path = project_root.getProjectRoot() + r"\resources\testdata\导出多语言路径" + "\\" + "点击超链"
        # 切换导出路径
        nav4_page.check_output_path(file_path)
        # 点击导出按钮
        nav4_page.export_click()

        if not nav4_page.export_succeeded_appear():
            logger.info("未找到音视频转换成功提示弹窗")
            assert False

        logger.info("已经找到音视频转换成功提示弹窗")
        control = active_window.GroupControl(ClassName='ExportWidget', Depth=1).CustomControl(
            ClassName='QStackedWidget', Depth=1).GroupControl(ClassName='ExportSuccess', Depth=1).ButtonControl(
            ClassName='CustomBtn', foundIndex=2, Depth=1)
        control_raise(control, "提示成功弹窗，openfolder按钮")
        nav4_page.click(control)
        time.sleep(3)
        # 关闭，点击超链弹出的文件资源管理器
        element1 = ScreenElement(GetPath().getImagePath("nav4_file_voice_changer/link.png"))
        if element1.exists():
            logger.info("已经打开文件资源管理器")
            assert True
        else:
            logger.info("未打开文件资源管理器")
            assert False







