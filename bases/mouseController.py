#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : mouseController.py

import uiautomation as auto
import random
import time

from commons.utils.myLogging import get_logger

# 配置日志
logger = get_logger()


class SlowMouseController:
    """
    缓慢鼠标控制器
    """

    def __init__(self):

        self.speed = 0.01  # 默认移动间隔（秒）

    def move_to(self, x, y, duration=1.0):
        """缓慢移动到指定位置"""
        current_x, current_y = auto.GetCursorPos()
        steps = max(int(duration / self.speed), 5)

        step_x = (x - current_x) / steps
        step_y = (y - current_y) / steps

        for i in range(steps):
            new_x = int(current_x + step_x * (i + 1))
            new_y = int(current_y + step_y * (i + 1))
            auto.SetCursorPos(new_x, new_y)
            # 添加随机延迟，更像人类操作
            time.sleep(self.speed + random.uniform(0, 0.02))

    def click(self, x, y, duration=1.0, clicks=1):
        """
        缓慢移动并点击
        :param duration: 移动时间
        :param clicks: 点击次数
        """

        # 移动
        self.move_to(x, y, duration)

        # 停顿
        time.sleep(random.uniform(0.1, 0.3))

        # 点击
        for i in range(clicks):
            auto.Click(x, y, waitTime=0.1)
            if i < clicks - 1:
                time.sleep(random.uniform(0.1, 0.2))

        logger.info(f"完成{clicks}次点击({x}, {y})")

    def double_click(self, x, y, duration=1.0):
        """双击"""
        self.click(x, y, duration, clicks=2)

    def right_click(self, x, y, duration=1.0):
        """右键点击"""
        self.move_to(x, y, duration)
        time.sleep(random.uniform(0.1, 0.3))
        auto.RightClick(x, y)


if __name__ == '__main__':
    # 使用示例
    controller = SlowMouseController()
    controller.click(500, 300, duration=6.0)
    controller.double_click(600, 400, duration=1.5)
    controller.right_click(700, 500, duration=1.0)
