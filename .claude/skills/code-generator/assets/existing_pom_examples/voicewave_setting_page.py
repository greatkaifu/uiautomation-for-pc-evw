#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_setting_page.py
import uiautomation as auto

from bases.basePage import  BasePage
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger

logger = get_logger()

project_path = GetPath()


class VoicewaveSettingPage(BasePage):
    """
    Setting页面操作封装
    """

    def __int__(self, main_window):
        super().__init__(main_window)

    def click_microphone_combobox(self):
        """
        在Setting页，点击麦克风下拉框
        :return:
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ComboBoxControl(
            ClassName='QComboBox', Depth=7)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到麦克风下拉框控件")
        BasePage.click(self, control)
        logger.info("已点击麦克风下拉框")

    def click_speaker_combobox(self):
        """
        在Setting页，点击扬声器下拉框
        :return:
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ComboBoxControl(
            ClassName='QComboBox', foundIndex=2, Depth=7)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到扬声器下拉框控件")
        BasePage.click(self, control)
        logger.info("已点击扬声器下拉框")

    def click_nav_list_item(self):
        """
        点击左侧导航栏ListItem
        """
        control = self.main_window.ListControl(ClassName='CNaviListWidget', Depth=5).ListItemControl(Depth=1)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到导航栏ListItem控件")
        BasePage.click(self, control)
        logger.info("已点击导航栏ListItem")

    def click_translate_tab(self):
        """
        在Setting页，点击翻译设置TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='TabsWidget', foundIndex=1, Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(
            ClassName='TabButton', Depth=3)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到Setting页TabButton控件")
        BasePage.click(self, control)
        logger.info("已点击Setting页翻译TabButton")

    def click_translate_scroll_area(self):
        """
        在Setting翻译页，点击滚动区域使滚动区域获取焦点
        """
        control = self.main_window.GroupControl(ClassName='QScrollArea', foundIndex=2)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到翻译页滚动区域控件")
        BasePage.click(self, control)
        logger.info("已点击翻译页滚动区域，获取焦点")

    def click_second_tab(self):
        """
        在Setting页，点击第二个TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='TabsWidget', foundIndex=1, Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(
            ClassName='TabButton', foundIndex=2, Depth=3)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到Setting页第二个TabButton控件")
        BasePage.click(self, control)
        logger.info("已点击Setting页第二个TabButton")

    def find_second_list_item(self):
        """
        在Setting页内容区域，查找第二个ListItem控件
        :return: True 找到控件，False 未找到
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ListItemControl(
            foundIndex=2, Depth=4)
        result = BasePage.find_control(self, control)
        return result

    def find_first_list_item(self):
        """
        在Setting页内容区域，查找第一个ListItem控件
        :return: True 找到控件，False 未找到
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).ListItemControl(
            foundIndex=1, Depth=4)
        result = BasePage.find_control(self, control)
        return result

    def click_general_tab(self):
        """
        在Setting页，点击General TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(
            ClassName='TabButton', Depth=6)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到General TabButton控件")
        BasePage.click(self, control)
        logger.info("已点击General TabButton")

    def find_translate_text_by_scroll(self):
        """
        通过滚轮查找翻译相关文本控件
        :return: True 找到控件，False 未找到
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(
            Name='Enable to automatically translate user-created voicecontent based on your installed language.',
            ClassName='QLabel', foundIndex=2, Depth=4)
        result = BasePage.find_control_by_scroll_up_and_down(self, control, max_scroll_down=50, max_scroll_up=50, scroll_interval=0.5, scroll_amount=50)
        return result

    def click_setting_general_tab(self):
        """
        在Setting页，通过SettingWidget内的TabsWidget点击General TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='SettingWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.SettingWidget', Depth=1).GroupControl(
            ClassName='TabsWidget', Depth=1).GroupControl(
            ClassName='QScrollArea', Depth=1).ButtonControl(
            ClassName='TabButton', Depth=3)
        if not auto.WaitForExist(control, 5):
            raise LookupError("未找到Setting页General TabButton控件")
        BasePage.click(self, control)
        logger.info("已点击Setting页General TabButton")

    def find_headphone_label(self):
        """
        在General页，查找耳机选择标签
        :return: 控件对象
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(
            ClassName='QStackedWidget', Depth=2).GroupControl(
            ClassName='QWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.SettingWidget.stackedWidget.w2194223549920.qt_scrollarea_viewport.genArea.widget_deviceCtlRect.widget_6.widget_deviceSetting.widget_headphoneRect', Depth=7).TextControl(
            Name='Please select your headphone:', ClassName='QLabel', Depth=1)
        return control

    def find_microphone_label(self):
        """
        在General页，查找麦克风选择标签
        :return: 控件对象
        """
        control = self.main_window.GroupControl(ClassName='SettingWidget').TextControl(
            Name='Please select your microphone:', ClassName='QLabel')
        return control

    def click_settings_nav(self):
        """
        点击左侧栏设置功能控件
        """
        control = self.main_window.GroupControl(ClassName='PageSelWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.widget_Sel', Depth=4).ListControl(ClassName='CNaviListWidget', Depth=1).ListItemControl(foundIndex=6, Depth=1)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info("已点击左侧栏设置功能控件。")
                return True
            else:
                logger.error("未找到左侧栏设置功能控件。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到左侧栏设置功能控件。")
            return None

    def click_shortcuts_tab(self):
        """
        在Setting页，点击快捷键TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='SettingWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.SettingWidget', Depth=1).GroupControl(ClassName='TabsWidget', Depth=1).GroupControl(ClassName='QScrollArea', Depth=1).ButtonControl(ClassName='TabButton', foundIndex=2, Depth=3)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info("已点击快捷键TabButton。")
                return True
            else:
                logger.error("未找到快捷键TabButton。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到快捷键TabButton。")
            return None

    def find_keybind_list_item(self):
        """
        在快捷键页，查找快捷键列表ListItem控件
        :return: True 找到控件，None 未找到
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).ListItemControl(Depth=5)
        result = self.find_control(control)
        return result

    def click_general_tab_btn(self):
        """
        在Setting页，点击General TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='TabsWidget', Depth=2).ButtonControl(ClassName='TabButton', Depth=4)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info("已点击General TabButton。")
                return True
            else:
                logger.error("未找到General TabButton。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到General TabButton。")
            return None

    def click_general_page_label(self):
        """
        在General页，点击QLabel控件获取焦点
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).TextControl(ClassName='QLabel', Depth=8)
        try:
            if self.find_control(control):
                self.click(control)
                logger.info("已点击General页QLabel控件。")
                return True
            else:
                logger.error("未找到General页QLabel控件。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error("未找到General页QLabel控件。")
            return None

    def find_dot_by_scroll(self):
        """
        在General页，通过滚轮查找圆点图片
        :return: True 找到图片，None 未找到
        """
        result = self.find_element_by_scroll_up_and_down('nav6_settings/圆点.png', max_scroll_down=50, max_scroll_up=50)
        logger.info(f"滚动查找圆点图片结果: {result}")
        return result
