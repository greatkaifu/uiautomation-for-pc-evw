#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_home_page.py.py

# 具体页面（业务封装）
import subprocess
import time

from bases.basePage import BasePage

import uiautomation as auto

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath

from commons.utils.killProcess import kill_process_by_name
from commons.utils.readconfig import INIConfigReader
from commons.utils.myLogging import get_logger

logger = get_logger()


project_path=GetPath()

class UserLoginPage(BasePage):
    """
    EaseUS VoiceWave

    用户登录页操作封装

    """
    def __int__(self, main_window):
        super().__init__(main_window)


    def click_login_icon(self):
        """
        在title栏，点击用户登录入口
        :return:
        """
        control = self.main_window.GroupControl(ClassName='MainWidgetTitle', Depth=1).ButtonControl(ClassName='UserAvatarButton', Depth=3)
        if auto.WaitForExist(control, 5):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击title栏，登录入口")
            return  True
        else:
            logger.info(f"未找到登录入口")
            return None

    def close_login_wait_alert(self):
        """
        关闭登录等待弹窗
        :return:
        """
        control = self.main_window.GroupControl(ClassName='LoginStatusDialog', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        if auto.WaitForExist(control, 5):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击登录等待弹窗关闭按钮")
            return  True
        else:
            logger.info(f"未找到登录等待弹窗的关闭按钮")
            return None

    def logout(self,path, x, y):
        """
        为了测试多言，通过图片识别处理
        公共方法
        center: 查找图片的中心点坐标
        相对于图片的中心偏移量计算出目标坐标点

        """
        project_path=GetPath()
        template_path = path
        try:
            # 拼接完整图片路径（字符串）
            position = ScreenElement(project_path.getImagePath(template_path))
            # #找到该图标
            if position.exists():
                # 计算找到图标的坐标，相对位置点击
                position.click_relative_to_element(offset_x=x, offset_y=y)

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_path.getImagePath(template_path)} 图标")

    def logout_alert_ok(self,path, x, y):
        """
        退出登录弹窗，点击确定按钮
        :return:
        """
        project_path = GetPath()
        template_path = path
        try:
            # 拼接完整图片路径（字符串）
            position = ScreenElement(project_path.getImagePath(template_path))
            # 找到该图标
            if position.exists():
                # 计算找到图标的坐标，相对位置点击
                position.click_relative_to_element(offset_x=x, offset_y=y)

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_path.getImagePath(template_path)} 图标")

    def close_btn(self,path):
        """
        退出登录弹窗，点击确定按钮
        :return:
        """
        template_path = path
        try:
            # 拼接完整图片路径（字符串）
            position = ScreenElement(project_path.getImagePath(template_path))
            # 获取图标的坐标
            position.click(delay=1)

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_path.getImagePath(template_path)} 图标")
