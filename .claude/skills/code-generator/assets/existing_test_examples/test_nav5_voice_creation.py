#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : leikaifu
# @File    : test_creat$
# @Time    : 2026/3/24$ 21:09$
# @IDE     : PyCharm
import allure
import pytest

from commons.utils.getProjectRroot import GetPath
from commons.utils.targetNotFoundError import control_raise, element_raise
from pom.voicewave_voice_creation_page import VoicewaveVoiceCreationPage

project_root = GetPath()

class TestNav5Creation:
    """
    克隆音效
    """
    @pytest.mark.test
    @allure.story("克隆音效")
    @allure.title("进入克隆页面-Create AI voice控件正常显示")
    def test_clone_sound(self, active_window):
        """
        克隆音效
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，clone按钮控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 查找 Create AI voice 控件
        create_ai_voice_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(Name='Create AI voice', ClassName='QLabel', Depth=4)
        result = nav5_page.find_control(create_ai_voice_control, 5)
        assert result == True

    @pytest.mark.test

    @allure.story("克隆上传音频")
    @allure.title("克隆页面-上传2min音频-continue图片正常出现")
    @pytest.mark.dependency(name="test_clone_upload_voice")
    def test_clone_upload_voice(self, active_window):
        """
        进入克隆页面上传音频页面，如果上传控件存在则上传音频，continue.png出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，clone按钮控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 查找 Click to upload voice files 控件
        nav5_page.click_upload_voice()
        # 在文件管理器中输入路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("2min.wav")
        # 检查 continue.png 是否出现
        result = nav5_page.find_element("nav5_voice_vreation/continue.png", timeout=30)
        assert result == True

    @allure.story("克隆删除已上传音频")
    @allure.title("克隆页面-点击delete删除已上传音频-continue图片消失")
    @pytest.mark.dependency(depends=["test_clone_upload_voice"])
    def test_clone_delete_voice(self, active_window):
        """
        点击delete图片删除已上传音频，continue图片不存在则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击delete图片
        nav5_page.find_element_and_click("nav5_voice_vreation/delete.png")
        # 检查 continue.png 是否不存在
        result = nav5_page.find_element("nav5_voice_vreation/continue.png")
        assert result == False

    @allure.story("克隆点击Continue按钮")
    @allure.title("克隆页面-上传音频后点击Continue-Create按钮正常出现")
    @pytest.mark.dependency(name="test_clone_click_continue")
    def test_clone_click_continue(self, active_window):
        """
        进入克隆页面，上传音频，点击Continue按钮，Create按钮出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，clone按钮控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 查找 Click to upload voice files 控件并上传
        result = nav5_page.click_upload_voice()
        assert result == True
        file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("2min.wav")
        # 等待 continue 图片出现
        result = nav5_page.find_element("nav5_voice_vreation/continue.png", timeout=30)
        assert result == True
        # 点击 Continue 按钮
        nav5_page.click_continue_btn()
        # 查找 Create 按钮控件
        create_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Create', ClassName='CustomBtn', Depth=7)
        result = nav5_page.find_control(create_btn, 10)
        assert result == True

    @allure.story("克隆点击Back按钮")
    @allure.title("克隆页面-点击Back按钮-返回上传音频页-continue图片正常出现")
    @pytest.mark.dependency(name="test_clone_click_back", depends=["test_clone_click_continue"])
    def test_clone_click_back(self, active_window):
        """
        点击Back按钮返回，continue图片出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击 Back 按钮
        nav5_page.click_back_btn()
        # 检查 continue.png 是否出现
        result = nav5_page.find_element("nav5_voice_vreation/continue.png")
        assert result == True

    @allure.story("克隆点击Continue后检查public图片")
    @allure.title("克隆页面-点击Continue进入信息填写页-public图片正常出现")
    @pytest.mark.dependency(name="test_clone_continue_public", depends=["test_clone_click_back"])
    def test_clone_continue_public(self, active_window):
        """
        点击Continue按钮，public图片出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击 Continue 按钮
        nav5_page.click_continue_btn()
        # 检查 public.png 是否出现
        result = nav5_page.find_element("nav5_voice_vreation/public.png")
        assert result == True

    @allure.story("克隆输入Voice名称并选择Anime标签")
    @allure.title("克隆页面-输入名称选择Anime标签上传图片-Create按钮可操作状态")
    @pytest.mark.dependency(name="test_clone_input_voice_name", depends=["test_clone_continue_public"])
    def test_clone_input_voice_name(self, active_window):
        """
        在输入框输入名称test123，选择Anime标签，tag图片出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击输入框并输入 test123
        input_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).EditControl(ClassName='QLineEdit', Depth=8)
        nav5_page.find_control_and_input(input_control, "test123")
        # 点击 Sound_tag 控件
        sound_tag = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=3, Depth=7).GroupControl(ClassName='QWidget', Depth=3)
        nav5_page.click(sound_tag)
        # 点击 Anime 图片
        nav5_page.find_element_and_click("nav5_voice_vreation/Anime.png")
        # 检查 tag.png 是否出现
        result = nav5_page.find_element("nav5_voice_vreation/tag.png")
        # 再次点击标签分组控件
        nav5_page.click(sound_tag)
        # 在描述输入框输入内容
        desc_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=4, Depth=7).EditControl(ClassName='QTextEdit', Depth=1)
        nav5_page.find_control_and_input(desc_control, "Wait and Retry: Server glitches often resolve within a few seconds or minutes.Check Status Pages: Verify if the API provider is experiencing a widespread outage.Reduce Payload Size: Large inputs, long prompts, or massive file uploads can trigger timeouts.Review API Parameters: Ensure your request complies with the required formatting and tokens limits.To help debug this, could you share which API you are using and the code snippet or payload that triggered the error?")
        # 点击 Upload image 按钮
        upload_img_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=5, Depth=7).ButtonControl(Name='Upload image', ClassName='QPushButton', Depth=3)
        nav5_page.click(upload_img_btn)
        # 在文件管理器中输入路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\images\nav5_voice_vreation"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("p2.png")
        # 检查 Create.png 是否出现
        result = nav5_page.find_element("nav5_voice_vreation/Create.png")
        assert result == True

    @allure.story("克隆点击Create按钮")
    @allure.title("克隆页面-点击Create按钮-进入训练页面-Cancel training task控件出现")
    @pytest.mark.dependency(name="test_clone_click_create", depends=["test_clone_input_voice_name"])
    def test_clone_click_create(self, active_window):
        """
        点击Create按钮，等待Cancel training task控件出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击 Create 按钮
        create_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Create', ClassName='CustomBtn', Depth=7)
        nav5_page.click(create_btn)
        # 等待 Cancel training task 控件出现
        cancel_training_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Cancel training task', ClassName='QPushButton', Depth=7)
        result = nav5_page.wait_for_control_appear(cancel_training_btn, 300)
        assert result == True

    @allure.story("克隆点击Cancel training task按钮")
    @allure.title("克隆页面-点击Cancel training task按钮-取消训练确认弹窗正常弹出")
    @pytest.mark.dependency(name="test_clone_cancel_training", depends=["test_clone_click_create"])
    def test_clone_cancel_training(self, active_window):
        """
        点击Cancel training task按钮，关闭按钮出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击 Cancel training task 按钮
        cancel_training_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Cancel training task', ClassName='QPushButton', Depth=7)
        nav5_page.click(cancel_training_btn)
        # 查找关闭按钮控件
        close_btn = active_window.GroupControl(ClassName='CancelTrainingConfirmDialog', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        result = nav5_page.find_control(close_btn, 5)
        assert result == True

    @allure.story("克隆关闭取消训练确认弹窗")
    @allure.title("克隆页面-点击关闭按钮关闭取消训练确认弹窗-弹窗消失")
    @pytest.mark.dependency(depends=["test_clone_cancel_training"])
    def test_clone_close_cancel_dialog(self, active_window):
        """
        点击关闭按钮，Yes按钮不存在则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击关闭按钮
        close_btn = active_window.GroupControl(ClassName='CancelTrainingConfirmDialog', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        nav5_page.click(close_btn)
        # 查找 Yes 按钮控件是否不存在
        yes_btn = active_window.GroupControl(ClassName='CancelTrainingConfirmDialog', Depth=1).ButtonControl(Name='Yes', ClassName='CustomBtn', Depth=1)
        result = nav5_page.find_control(yes_btn, 3)
        assert result == False

    @allure.story("克隆点击No按钮关闭确认弹窗")
    @allure.title("克隆页面-点击No按钮关闭取消训练确认弹窗-弹窗消失")
    @pytest.mark.dependency(depends=["test_clone_cancel_training"])
    def test_clone_click_no_cancel_dialog(self, active_window):
        """
        点击No按钮，Yes按钮不存在则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 再次点击 Cancel training task 按钮
        cancel_training_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Cancel training task', ClassName='QPushButton', Depth=7)
        nav5_page.click(cancel_training_btn)
        # 点击 No 按钮
        no_btn = active_window.GroupControl(ClassName='CancelTrainingConfirmDialog', Depth=1).ButtonControl(Name='No', ClassName='CustomBtn', Depth=1)
        nav5_page.click(no_btn)
        # 查找 Yes 按钮控件是否不存在
        yes_btn = active_window.GroupControl(ClassName='CancelTrainingConfirmDialog', Depth=1).ButtonControl(Name='Yes', ClassName='CustomBtn', Depth=1)
        result = nav5_page.find_control(yes_btn, 3)
        assert result == False

    @allure.story("克隆点击Yes按钮确认取消训练")
    @allure.title("克隆页面-点击Yes按钮确认取消训练-返回克隆首页-CloneNowButton出现")
    @pytest.mark.dependency(depends=["test_clone_click_create"])
    def test_clone_click_yes_cancel_dialog(self, active_window):
        """
        点击Yes按钮确认取消训练，CloneNowButton出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        # 点击 Cancel training task 按钮
        cancel_training_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Cancel training task', ClassName='QPushButton', Depth=7)
        nav5_page.click(cancel_training_btn)
        # 点击 Yes 按钮
        yes_btn = active_window.GroupControl(ClassName='CancelTrainingConfirmDialog', Depth=1).ButtonControl(Name='Yes', ClassName='CustomBtn', Depth=1)
        nav5_page.click(yes_btn)
        # 等待 CloneNowButton 控件出现
        clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
        result = nav5_page.wait_for_control_appear(clone_btn, 30)
        assert result == True

    @allure.story("克隆上传12min音频触发时长提示弹窗")
    @allure.title("克隆页面-上传12min音频点击Continue-触发时长提示弹窗-OK按钮正常出现")
    def test_clone_upload_duration_notice(self, active_window):
        """
        独立进入克隆页面，上传12min音频，点击Continue，出现时长提示弹窗则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，CloneNowButton控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 进入Create AI voice页面，点击上传音频控件
        nav5_page.click_upload_voice()
        # 在文件管理器中输入路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("12min.wav")
        # 等待min图片出现
        nav5_page.find_element("nav5_voice_vreation/min.png", timeout=30)
        # 点击Continue按钮
        continue_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Continue', ClassName='CustomBtn', Depth=9)
        nav5_page.click(continue_btn)
        # 检查时长提示弹窗OK按钮是否出现
        ok_btn = active_window.GroupControl(ClassName='CloneUploadDurationNoticeDialog', Depth=1).ButtonControl(Name='OK', ClassName='CustomBtn', Depth=1)
        result = nav5_page.find_control(ok_btn, 5)
        assert result == True
        # 点击关闭弹窗按钮
        close_btn = active_window.GroupControl(ClassName='CloneUploadDurationNoticeDialog', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        nav5_page.click(close_btn)
        # 删除已上传的音频
        nav5_page.find_element_and_click("nav5_voice_vreation/delete.png")

    @allure.story("克隆进入训练页面检查Cancel training task控件")
    @allure.title("克隆页面-完整流程上传音频填写信息点击Create-成功进入训练页面")
    def test_clone_enter_training_page(self, active_window):
        """
        独立进入克隆页面，上传音频，填写信息，点击Create，Cancel training task控件存在则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，CloneNowButton控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 点击上传音频控件
        control_raise(
            active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(ClassName='QLabel', Depth=5),
            "克隆页面-上传音频控件", timeout=5)
        nav5_page.click_upload_voice()
        # 在文件管理器中输入路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("2min.wav")
        # 等待 continue 图片出现
        element_raise("nav5_voice_vreation/continue.png", "克隆页面-上传音频后continue图片", timeout=30)
        # 点击 Continue 按钮
        control_raise(
            active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(Name='Continue', ClassName='CustomBtn', Depth=4),
            "克隆页面-Continue按钮")
        nav5_page.click_continue_btn()
        # 点击输入框并输入名称
        input_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).EditControl(ClassName='QLineEdit', Depth=8)
        control_raise(input_control, "克隆页面-Voice名称输入框")
        nav5_page.find_control_and_input(input_control, "test123")
        # 点击 Sound_tag 控件
        sound_tag = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=3, Depth=7).GroupControl(ClassName='QWidget', Depth=3)
        control_raise(sound_tag, "克隆页面-Sound tag标签分组控件")
        nav5_page.click(sound_tag)
        # 点击 Anime 图片
        nav5_page.find_element_and_click("nav5_voice_vreation/Anime.png")
        # 再次点击标签分组控件关闭
        nav5_page.click(sound_tag)
        # 在描述输入框输入内容
        desc_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=4, Depth=7).EditControl(ClassName='QTextEdit', Depth=1)
        control_raise(desc_control, "克隆页面-描述输入框")
        nav5_page.find_control_and_input(desc_control, "Wait and Retry: Server glitches often resolve within a few seconds or minutes.Check Status Pages: Verify if the API provider is experiencing a widespread outage.Reduce Payload Size: Large inputs, long prompts, or massive file uploads can trigger timeouts.Review API Parameters: Ensure your request complies with the required formatting and tokens limits.To help debug this, could you share which API you are using and the code snippet or payload that triggered the error?")
        # 点击 Upload image 按钮
        upload_img_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=5, Depth=7).ButtonControl(Name='Upload image', ClassName='QPushButton', Depth=3)
        control_raise(upload_img_btn, "克隆页面-Upload image按钮")
        nav5_page.click(upload_img_btn)
        # 在文件管理器中输入路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\images\nav5_voice_vreation"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("p2.png")
        # 点击 Create 按钮
        create_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Create', ClassName='CustomBtn', Depth=7)
        control_raise(create_btn, "克隆页面-Create按钮")
        nav5_page.click(create_btn)
        # 检查 Cancel training task 控件是否存在
        cancel_training_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Cancel training task', ClassName='QPushButton', Depth=7)
        control_raise(cancel_training_btn, "克隆页面-Cancel training task控件", timeout=300)

    @allure.story("克隆输入名称选择Anime标签验证Create按钮态可操作状态")
    @allure.title("克隆页面-输入名称test123456选择Anime标签-Create按钮可操作状态")
    def test_clone_input_name_select_anime(self, active_window):
        """
        进入Create AI voice页面，输入名称test123456，选择Anime标签，Create图片出现则用例成功
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，CloneNowButton控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 点击上传音频控件
        control_raise(
            active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(ClassName='QLabel', Depth=5),
            "克隆页面-上传音频控件", timeout=5)
        nav5_page.click_upload_voice()
        # 在文件管理器中输入路径并打开文件
        file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
        nav5_page.input_file_path(file_path)
        nav5_page.open_file("2min.wav")
        # 等待 continue 图片出现
        element_raise("nav5_voice_vreation/continue.png", "克隆页面-上传音频后continue图片", timeout=30)
        # 点击 Continue 按钮
        control_raise(
            active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(Name='Continue', ClassName='CustomBtn', Depth=4),
            "克隆页面-Continue按钮")
        nav5_page.click_continue_btn()
        # 点击输入框并输入名称
        input_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).EditControl(ClassName='QLineEdit', Depth=8)
        control_raise(input_control, "克隆页面-Voice名称输入框")
        nav5_page.find_control_and_input(input_control, "test123456")
        # 点击 Sound_tag 控件
        sound_tag = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='QWidget', foundIndex=3, Depth=7).GroupControl(ClassName='QWidget', Depth=3)
        control_raise(sound_tag, "克隆页面-Sound tag标签分组控件")
        nav5_page.click(sound_tag)
        # 点击 Anime 图片
        nav5_page.find_element_and_click("nav5_voice_vreation/Anime.png")
        # 再次点击 Sound_tag 控件关闭标签选择面板
        nav5_page.click(sound_tag)
        # 检查 Create.png 是否出现
        result = nav5_page.find_element("nav5_voice_vreation/Create.png")
        assert result == True

