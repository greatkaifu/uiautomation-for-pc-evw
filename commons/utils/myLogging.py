#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : myLogging.py


import logging
import os
from logging.handlers import RotatingFileHandler

import logging
import os
import re
from logging.handlers import RotatingFileHandler


# ANSI 颜色代码（仅终端有效）
class Colors:
    BLUE = '\033[34m'  # info - 蓝色
    GREEN = '\033[32m'  # debug - 绿色
    YELLOW = '\033[33m'  # warning - 黄色
    RED = '\033[31m'  # error - 红色
    MAGENTA = '\033[35m'  # critical - 紫红
    RESET = '\033[0m'  # 重置颜色


# 自定义彩色 Formatter
class ColorFormatter(logging.Formatter):
    """根据日志级别添加不同颜色的 Formatter"""

    COLORS = {
        logging.DEBUG: Colors.GREEN,
        logging.INFO: Colors.BLUE,  # ✅ info 显示蓝色
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.MAGENTA,
    }

    def format(self, record):
        # 先使用父类格式化
        log_message = super().format(record)

        # 添加颜色代码
        color = self.COLORS.get(record.levelno, Colors.RESET)
        return f"{color}{log_message}{Colors.RESET}"


# 可选：去除 ANSI 代码的 Formatter（用于文件输出）
class PlainFormatter(logging.Formatter):
    """移除 ANSI 转义序列，确保文件日志干净"""

    # 匹配 ANSI 转义序列的正则
    ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def format(self, record):
        raw = super().format(record)
        return self.ANSI_ESCAPE.sub('', raw)


def get_logger(name=__name__):
    # 1. 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 2. 创建格式化器
    base_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # 控制台：带颜色
    console_formatter = ColorFormatter(base_format, datefmt='%Y-%m-%d %H:%M:%S')
    # 文件：纯文本（无颜色代码）
    file_formatter = PlainFormatter(base_format, datefmt='%Y-%m-%d %H:%M:%S')

    # 3. 控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # 4. 文件 Handler（轮转）
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)  # ✅ 使用无颜色 formatter

    # 5. 添加 Handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# 使用示例
if __name__ == "__main__":
    #实例化一个日志器
    logger = get_logger()
    logger.debug("这是一条调试信息（绿色）")
    logger.info("程序正常运行（🔵 蓝色）")  # ← 控制台显示蓝色
    logger.warning("这是一个警告（黄色）")
    logger.error("出错了！（红色）")
    logger.critical("严重错误！（紫红色）")