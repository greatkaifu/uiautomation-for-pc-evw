#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : browser.py


import time

import uiautomation as auto
from commons.utils.myLogging import get_logger
import time




# 实例化一个日志器
logger = get_logger()


class Browser:
    def __init__(self, timeout=10):
        # 支持动态配置等待超时时间
        self.timeout = timeout
        self.browser_configs = [
            {"id": "Edge", "class": "Chrome_WidgetWin_1", "name_re": ".*Microsoft\u200b Edge.*"},
            {"id": "Chrome", "class": "Chrome_WidgetWin_1", "name_re": ".*Google Chrome.*"},
            {"id": "Brave", "class": "Chrome_WidgetWin_1", "name_re": ".*Brave.*"},
            {"id": "Firefox", "class": "MozillaWindowClass", "name_re": ".*Firefox.*"}
        ]

    def _find_address_bar(self, window, browser_id):
        """内部辅助方法：根据浏览器类型定位地址栏"""
        # Chromium 系浏览器通用策略
        address_edit = window.EditControl(
            searchDepth=12,
            controlType=auto.ControlType.EditControl,
            searchInterval=0.5
        )

        # Firefox 特殊路径
        if browser_id == "Firefox" and not address_edit.Exists(0):
            combo = window.ComboBoxControl(searchDepth=15, searchInterval=0.5)
            if combo.Exists(0):
                address_edit = combo.EditControl(searchInterval=0.5)

        return address_edit

    def get_current_browser_url(self):
        """查找当前活动的浏览器并返回 ID、类名和 URL"""
        for config in self.browser_configs:
            window = auto.WindowControl(
                searchDepth=1,
                ClassName=config["class"],
                NameIsFull=False,
                RegexName=config["name_re"]
            )

            if window.Exists(maxSearchSeconds=2):
                window.SetFocus()
                time.sleep(0.3)  # 等待焦点切换生效

                address_bar = self._find_address_bar(window, config["id"])

                if address_bar.Exists(maxSearchSeconds=2):
                    try:
                        value_pattern = address_bar.GetValuePattern()
                        url = value_pattern.Value.strip() if value_pattern else ""

                        # 智能补全协议头
                        if url and not url.startswith(('http', 'file', 'about', 'chrome', 'edge')):
                            url = f"https://{url}"

                        return {
                            "browser": config["id"],
                            "url": url,
                            "class": config["class"],
                            "window_obj": window
                        }
                    except Exception as e:
                        logger.error(f"提取 URL 失败: {e}")
                        continue
        return None

    def close_browser(self, strategy="window", wait_seconds=1):
        """
        获取当前 URL 并关闭浏览器
        :param strategy: 'window' (Alt+F4) 或 'tab' (Ctrl+W)
        :param wait_seconds: 发送按键前的等待时间（秒）
        """
        info = self.get_current_browser_url()

        if not info:
            logger.warning("未检测到支持的浏览器窗口")
            return None

        window = info["window_obj"]
        logger.info(f"检测到 {info['browser']}，当前 URL: {info['url']}")

        # 确保窗口获得焦点
        window.SetFocus()
        window.SetActive()
        time.sleep(wait_seconds)

        if strategy == "window":
            logger.info(f"正在关闭整个 {info['browser']} 窗口 (Alt+F4)...")
            auto.SendKeys('{Alt}{F4}')
        elif strategy == "tab":
            logger.info(f"正在关闭 {info['browser']} 的当前标签页 (Ctrl+W)...")
            auto.SendKeys('{Ctrl}w')
        else:
            logger.warning(f"未知关闭策略: {strategy}，使用默认 window 策略")
            auto.SendKeys('{Alt}{F4}')

        # 可选：等待窗口关闭并验证
        time.sleep(0.5)
        return info

    def find_opened_url(self, target_url, normalize=True):
        """
        检查 URL 是否打开（支持智能等待和 URL 标准化）
        :param target_url: 目标 URL
        :param normalize: 是否自动清理空格并标准化比较
        """
        # 安全获取当前 URL
        info = self.get_current_browser_url()
        if not info:
            logger.warning(f"未检测到浏览器，无法查找 URL: {target_url}")
            return False

        current_url = info["url"]

        # URL 标准化处理（去除首尾空格、统一协议等）
        if normalize:
            target_url = target_url.strip()
            current_url = current_url.strip()
            # 可选：忽略末尾斜杠差异
            if target_url.rstrip('/') == current_url.rstrip('/'):
                logger.info(f"已找到目标 URL: {target_url}")
                return True
        else:
            if current_url == target_url:
                logger.info(f"已找到目标 URL: {target_url}")
                return True

        logger.warning(f"未匹配目标 URL")
        logger.warning(f"   期望: {target_url}")
        logger.warning(f"   实际: {current_url}")
        return False

    def close_by_url(self, target_url, strategy="window", max_retries=3):
        """
        高级方法：根据 URL 查找并关闭对应浏览器（带重试机制）
        """
        for attempt in range(max_retries):
            if self.find_opened_url(target_url):
                logger.info(f"尝试关闭浏览器 (第 {attempt + 1}/{max_retries} 次)...")
                result = self.close_browser(strategy=strategy)
                if result:
                    return True
            time.sleep(1)
        logger.error(f"重试 {max_retries} 次后仍未找到或关闭目标 URL")
        return False


# --- Example Usage ---
if __name__ == "__main__":
    inspector = Browser(timeout=10)
    target = "https://voicechanger.easeus.com/?&uid=S-1-5-21-4164000093-2963957314-936180009-1001"

    # # 方案1：分步调用（修复参数问题）
    # if inspector.find_opened_url(target):
    #     print(f"Found {target}, attempting to close...")
    #     time.sleep(1)
    #     # 正确传入 strategy 参数
    #     if inspector.close_browser(strategy="window"):
    #         print("Close signal sent.")

    # # 方案2：使用高级封装方法（推荐）
    # inspector.close_by_url(target, strategy="window")
    inspector.get_current_browser_url()
    logger.info(inspector.get_current_browser_url())

    logger.info(inspector.get_current_browser_url()["url"])