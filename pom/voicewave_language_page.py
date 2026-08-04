#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_language_page.py
import os
from datetime import datetime

from PIL import ImageGrab
# 具体页面（业务封装）
import subprocess
import time

from bases.basePage import BasePage

import uiautomation as auto
import os
import time
from typing import Optional, Tuple
from PIL.Image import Image
import cv2
import numpy as np
import pyautogui
import uiautomation
from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath

from commons.utils.killProcess import kill_process_by_name
from commons.utils.readconfig import INIConfigReader
from commons.utils.myLogging import get_logger

logger = get_logger()





class VoicewaveLanguagePage(BasePage):
    """EaseUS VoiceWave language 多语言操作封装"""


    def __int__(self, main_window):
        super().__init__(main_window)



    def capture_picture(self, language):
        """
        截图功能
        只截取程序区域的图片
        - 按 language 创建子文件夹
        - 截图文件使用时间戳命名
        """
        # 1. 配置基础路径
        base_dir = "./language_screenshots/导入功能"  # 截图根目录
        lang_dir = os.path.join(base_dir, language)  # 语言子目录

        # 2. 创建文件夹（如果不存在）
        os.makedirs(lang_dir, exist_ok=True)

        # 3. 找到目标窗口
        window = self.main_window

        if window.Exists(maxSearchSeconds=10):
            logger.info(f"[{language}] 找到窗口")

            # 4. 获取窗口坐标
            rect = window.BoundingRectangle
            logger.info(f"[{language}] 窗口坐标：{rect}")

            # 5. 截图
            screenshot = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))

            # 6. 生成时间戳文件名 (格式：English_20240115_143025_123.png)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{language}_{timestamp}.png"
            filepath = os.path.join(lang_dir, filename)

            # 7. 保存图片
            screenshot.save(filepath)
            logger.info(f"[{language}] 截图已保存：{filepath}")

            return filepath  # 返回保存路径，方便后续使用
        else:
            logger.info(f"[{language}] 未找到指定窗口")
            return None



    def capture_all_picture(self, language,region: Optional[Tuple[int, int, int, int]] = None):
        """
           截图功能，截取全屏
        - 按 language 创建子文件夹
        - 截图文件使用时间戳命名

        :param region: 截图区域 (x, y, width, height)，None 表示全屏
        :return: PIL.Image.Image 对象
        :raises RuntimeError: 截图失败时抛出
        """

        try:
            # 1. 配置基础路径
            base_dir = "./language_screenshots"  # 截图根目录
            lang_dir = os.path.join(base_dir, language)  # 语言子目录
            if region is not None:
                x, y, w, h = region
                if w <= 0 or h <= 0:
                    raise ValueError(f"区域尺寸无效: width={w}, height={h}")
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
                logger.info(f"[Screen] 截图区域: ({x}, {y}, {w}, {h})")
                # 生成时间戳文件名 (格式：20240115_143025_123.png)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"{timestamp}.png"
                filepath = os.path.join(lang_dir, filename)

                # 保存图片
                screenshot.save(filepath)
                logger.info(f"[{language}] 截图已保存：{filepath}")
                # 截取图片成功
                return True
            else:
                # 如果区域参数为None  就截全图
                screenshot = pyautogui.screenshot()
                # 生成时间戳文件名 (格式：20240115_143025_123.png)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"{timestamp}.png"
                filepath = os.path.join(lang_dir, filename)

                # 保存图片
                screenshot.save(filepath)
                logger.info(f"[{language}] 截图已保存：{filepath}")
                # 截取图片成功
                return True  #

        except Exception as e:
            raise RuntimeError(f"截图失败: {e}") from e

    def click_ai(self,path):
        """
        点击按钮
        """
        template_path = path
        project_path = GetPath()
        try:
            # 拼接完整图片路径（字符串）


            position = ScreenElement(project_path.getImagePath(template_path))
            # 找到该图标，点击操作
            position.click(delay=1)

        except Exception as e:
            logger.error(f"{e}")
            logger.info(f"未找到 {project_path.getImagePath(template_path)} 图标")

