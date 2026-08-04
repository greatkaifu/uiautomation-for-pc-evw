#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : readconfig.py

import configparser
import os
from commons.utils.myLogging import get_logger
import configparser

# 配置日志（适配中文环境）
from commons.utils.getProjectRroot import GetPath

logger = get_logger()

path=GetPath()

class INIConfigReader:
    def __init__(self, encoding='utf-8-sig'):
        self.config_path = path.getconfiginiPath("config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(path.getconfiginiPath("config.ini"), encoding=encoding)

    def getconfig(self, section, option):
        """读取配置项 - 直接使用当前实例"""
        try:
            return self.config.get(section, option)
        except Exception as e:
            raise RuntimeError(f"配置读取失败 [{section}.{option}]: {e}") from e


if __name__ == '__main__':
    reader = INIConfigReader()
    path = reader.getconfig('install', 'path')
    logger.info(path)

