#!/usr/bin/python3
# -*- coding : utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn

"""
屏幕 UI 元素自动化操作类（基于图像模板匹配）
适用于 Windows 环境下的 UI 自动化任务，如点击按钮、查找图标等。
依赖：pyautogui, opencv-python, numpy, uiautomation, Pillow
"""
import os
import time
from typing import Optional, Tuple
import cv2
import numpy as np
import pyautogui
import uiautomation as auto

# pyautogui.screenshot() 返回的是 PIL.Image.Image 对象，它默认是 RGB 模式。
# 而 OpenCV 默认使用 BGR 模式，所以你需要做 RGB → BGR 转换。
from bases.mouseController import SlowMouseController

from commons.utils.myLogging import get_logger
from commons.utils.getProjectRroot import GetPath

logger = get_logger()


class ScreenElement:
    """
    表示一个由模板图片定义的屏幕 UI 元素。
    实例化后，所有操作均针对该元素。
    """

    def __init__(
            self,
            template_path: str,
            threshold: float = 0.9,
            delay: float = 1.0,
            debug: bool = True
    ):
        """
        初始化屏幕元素

        :param template_path: 模板图片路径（必须存在）
        :param threshold: 匹配阈值，0.0 ~ 1.0，默认 0.9
        :param delay: 操作后默认等待时间（秒），默认 1.0
        :param debug: 是否保存调试截图（screen_debug.png）
        :raises FileNotFoundError: 模板文件不存在
        """
        abs_path = os.path.abspath(template_path)
        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"模板文件不存在: {abs_path}")
        self.template_path = abs_path
        self.threshold = threshold
        self.delay = delay
        self.debug = debug
        logger.info(f"[初始化] 已加载模板: {self.template_path}")

    def _take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None):
        """
        Partial area
        内部方法：截取屏幕区域

        :param region: 截图区域 (x, y, width, height)，None 表示全屏
        :return: PIL.Image.Image 对象
        :raises RuntimeError: 截图失败时抛出
        """
        try:
            if region is not None:
                x, y, w, h = region
                if w <= 0 or h <= 0:
                    raise ValueError(f"区域尺寸无效: width={w}, height={h}")
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
                logger.info(f"[Screen] 截图区域: ({x}, {y}, {w}, {h})")
                # 保存截图用于调试,方便定位调试错误
                screenshot.save('screen.png')
            else:
                # 如果区域参数为None  就截全图
                screenshot = pyautogui.screenshot()
                # 保存截图用于调试,方便定位调试错误
                screenshot.save('screen.png')

            return screenshot

        except Exception as e:
            raise RuntimeError(f"截图失败: {e}") from e

    def find(
            self,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None,
            save_debug: Optional[bool] = None
    ) -> Optional[Tuple[int, int]]:
        """
        在屏幕上查找当前元素位置

        :param region: 截图区域 (x, y, width, height)
        :param threshold: 临时覆盖匹配阈值
        :param save_debug: 是否保存调试截图（None 表示使用初始化设置）
        :return: (x, y) 坐标，未找到返回 None
        """
        th = threshold if threshold is not None else self.threshold
        debug_save = save_debug if save_debug is not None else self.debug

        try:
            screenshot = self._take_screenshot(region)

            # 直接转换为numpy数组
            screenshot_np = np.array(screenshot)
            # 转换颜色格式（PIL -> OpenCV）
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

            # 读取模板
            template = cv2.imread(self.template_path)
            if template is None:
                logger.error(f"[错误] 无法加载模板图片: {self.template_path}")
                return None

            # 模板匹配
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            logger.info(f"[Match] 得分: {max_val:.3f}, 阈值: {th}")

            if max_val >= th:
                h, w = template.shape[:2]
                if region:
                    x = max_loc[0] + w // 2 + region[0]
                    y = max_loc[1] + h // 2 + region[1]
                else:
                    x = max_loc[0] + w // 2
                    y = max_loc[1] + h // 2
                logger.info(f"[Found] 元素中心坐标: ({int(x)}, {int(y)})")
                return (int(x), int(y))
            else:
                logger.info(f"[Not Found] 匹配度不足 ({max_val:.3f} < {th})")
                return None

        except Exception as e:
            logger.error(f"[异常] 查找失败: {e}")
            return None

    def exists(
            self,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None,
            timeout: float = 0
    ) -> bool:
        """
        判断元素是否存在（不保存调试图），支持超时等待

        :param region: 截图区域 (x, y, width, height)
        :param threshold: 临时覆盖匹配阈值
        :param timeout: 超时时间（秒），默认0即不等待只查找一次
        :return: 存在返回 True，不存在返回 False
        """
        end_time = time.time() + timeout
        while True:
            if self.find(region, threshold, save_debug=False) is not None:
                return True
            if time.time() >= end_time:
                return False
            time.sleep(0.5)

    def click(
            self,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None,
            delay: Optional[float] = None,
            timeout: float = 0
    ) -> bool:
        """
        查找并点击元素，支持超时等待

        :param region: 截图区域 (x, y, width, height)
        :param threshold: 临时覆盖匹配阈值
        :param delay: 点击后等待时间（秒），None时使用实例默认值
        :param timeout: 超时时间（秒），默认0即不等待只查找一次
        :return: 是否成功点击
        """
        end_time = time.time() + timeout
        while True:
            pos = self.find(region, threshold)
            if pos:
                pyautogui.click(pos[0], pos[1], duration=1, tween=pyautogui.easeOutQuad)
                time.sleep(delay or self.delay)
                logger.info(f"[Click] 已点击坐标: {pos}")
                return True
            if time.time() >= end_time:
                logger.info("[Click] 未找到元素，点击失败")
                return False
            time.sleep(0.5)

    def move_to_position(
            self,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None,
            delay: Optional[float] = None,
            timeout: float = 0
    ) -> bool:
        """
        查找并移动到元素坐标点，支持超时等待

        :param region: 截图区域 (x, y, width, height)
        :param threshold: 临时覆盖匹配阈值
        :param delay: 移动后等待时间（秒），None时使用实例默认值
        :param timeout: 超时时间（秒），默认0即不等待只查找一次
        :return: 是否移动成功
        """
        end_time = time.time() + timeout
        while True:
            pos = self.find(region, threshold)
            if pos:
                pyautogui.moveTo(pos[0], pos[1], duration=1, tween=pyautogui.easeOutQuad)
                time.sleep(delay or self.delay)
                logger.info(f"已经移动到坐标位置: {pos}")
                return True
            if time.time() >= end_time:
                logger.info("未找到元素，移动失败")
                return False
            time.sleep(0.5)

    def double_click(
            self,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None,
            delay: Optional[float] = None,
            timeout: float = 0
    ) -> bool:
        """
        查找并双击元素，支持超时等待

        :param region: 截图区域 (x, y, width, height)
        :param threshold: 临时覆盖匹配阈值
        :param delay: 双击后等待时间（秒），None时使用实例默认值
        :param timeout: 超时时间（秒），默认0即不等待只查找一次
        :return: 是否成功双击
        """
        end_time = time.time() + timeout
        while True:
            pos = self.find(region, threshold)
            if pos:
                pyautogui.doubleClick(pos[0], pos[1], duration=1, tween=pyautogui.easeOutQuad)
                time.sleep(delay or self.delay)
                logger.info(f"[DoubleClick] 已双击坐标: {pos}")
                return True
            if time.time() >= end_time:
                logger.info("[DoubleClick] 未找到元素，双击失败")
                return False
            time.sleep(0.5)

    def scroll_and_find(
            self,
            max_scroll_down: int = 20,
            max_scroll_up: int = 20,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None
    ) -> bool:
        """
        滚动查找元素（先向下滚动，再向上回溯）
        max_scroll_down  可调参数
        max_scroll_up    可调参数
        :return: 是否找到
        """
        if self.exists(region, threshold):
            logger.info("[ScrollFind] 首次查找即命中")
            return True

        logger.info("[ScrollFind] 开始向下滚动...")
        for i in range(max_scroll_down):
            logger.info(f"[Scroll] 向下第 {i + 1} 次")
            auto.WheelDown(wheelTimes=1)
            time.sleep(0.3)
            if self.exists(region, threshold):
                logger.info(f"[ScrollFind] 向下滚动 {i + 1} 次后找到")
                return True

        logger.info("[ScrollFind] 开始向上回溯...")
        for j in range(max_scroll_up):
            logger.info(f"[Scroll] 向上第 {j + 1} 次")
            auto.WheelUp(wheelTimes=1)
            time.sleep(0.3)
            if self.exists(region, threshold):
                logger.info(f"[ScrollFind] 向上滚动 {j + 1} 次后找到")
                return True

        logger.error("[ScrollFind] 滚动完毕仍未找到目标元素")
        return False

    def click_relative_to_element(
            self,
            offset_x: int = 0,
            offset_y: int = 0,
            timeout: float = 10.0,
            interval: float = 0.5,
            region: Optional[Tuple[int, int, int, int]] = None,
            threshold: Optional[float] = None,
    ) -> bool:
        """
        相对于元素中心偏移量点击。

        之前的实现会在 find() 返回 None 时仍访问 center[0]/center[1]，
        导致 TypeError: 'NoneType' object is not subscriptable。
        这里改为：在 timeout 内重试查找；超时则抛出明确异常。
        """
        start = time.time()
        center: Optional[Tuple[int, int]] = None
        while time.time() - start <= timeout:
            center = self.find(region=region, threshold=threshold)
            if center is not None:
                break
            time.sleep(interval)

        if center is None:
            raise TimeoutError(
                f"在 {timeout}s 内未匹配到模板图，无法相对点击。template={self.template_path}, "
                f"threshold={threshold if threshold is not None else self.threshold}, region={region}"
            )

        target_x = center[0] + offset_x
        target_y = center[1] + offset_y

        mouse = SlowMouseController()
        mouse.click(target_x, target_y, duration=1.0, clicks=1)
        logger.info(f"已点击元素相对位置: ({offset_x}, {offset_y})")
        return True



    # 不用
    @staticmethod
    def move_to(x: int, y: int, wait_time: float = 0.5):
        """移动鼠标到指定坐标"""
        auto.MoveTo(x, y, waitTime=wait_time)

    @staticmethod
    def send_keys(keys: str, wait_time: float = 0.5):
        """发送键盘按键"""
        auto.SendKeys(keys, waitTime=wait_time)

    @staticmethod
    def click_coord(x: int, y: int, wait_time: float = 0.5):
        """直接点击坐标"""
        auto.Click(x, y, waitTime=wait_time)


if __name__ == "__main__":
    main_win = auto.WindowControl(Name='FocalFlow 录制', ClassName='RecordMainWindow_QMLTYPE_25_QML_73', Depth=1)
    if not main_win.Exists(maxSearchSeconds=30):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)
    # main_win.SetActive()
    project_path = GetPath()
    time.sleep(6)
    template_path = project_path.getImagePath("nav4_file_voice_changer/close_btn.png")

    position = ScreenElement(GetPath().getImagePath(template_path))
    # 找到该图标，点击操作
    # position.click(delay=1)
    #
    if position.find():
        position.click_relative_to_element(offset_x=70, offset_y=0)
