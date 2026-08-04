#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : targetNotFoundError.py
import uiautomation

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath

project_root = GetPath()

class TargetControlNotFoundError(RuntimeError):
    """未找到目标 UI 控件时抛出，message 中应包含控件描述。"""


def control_raise(control: uiautomation.Control, description: str, timeout: float = 10) -> uiautomation.Control:
    """
    验证 UI 控件必须存在，不存在则抛出异常。在 timeout 内持续轮询查找，等待控件完全显示。
    :param control: uiautomation.Control 控件对象
    :param description: 控件中文描述，用于异常提示定位失败步骤
    :param timeout: 最大等待时间（秒），默认 10s
    :return: 控件对象
    :raises TargetControlNotFoundError: 控件在超时内未出现时抛出
    """
    if not uiautomation.WaitForExist(control, timeout):
        raise TargetControlNotFoundError(
            f"未找到目标元素：{description} 超时 {timeout}s"
        )
    return control



class TargetElementNotFoundError(RuntimeError):
    """未找到目标 UI 控件时抛出，message 中应包含控件描述。"""

def element_raise(template_path, description: str, timeout: float = 10, interval: float = 0.5):
    """
    验证图片/图标必须存在，不存在则抛出异常。在 timeout 内持续轮询查找，等待界面渲染完成。
    :param template_path: 图片相对路径，如 "nav5_voice_vreation/Anime.png"（内部自动拼接 resources/images 根目录）
    :param description: 元素中文描述，用于异常提示定位失败步骤
    :param timeout: 最大等待时间（秒），默认 10s
    :param interval: 轮询间隔（秒），默认 0.5s
    :return: True
    :raises TargetElementNotFoundError: 图片在超时内未匹配到时抛出
    """
    import time
    # 拼接完整图片绝对路径（项目根目录/resources/images/ + template_path）
    full_path = project_root.getImagePath(template_path)
    start_time = time.time()
    while time.time() - start_time < timeout:
        if ScreenElement(full_path).exists(timeout=0):
            return True
        time.sleep(interval)
    raise TargetElementNotFoundError(
        f"未找到目标元素：{description} 超时 {timeout}s"
    )
