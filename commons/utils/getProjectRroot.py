#!/usr/bin/python3
# -*- coding : utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn

import os
from pathlib import Path
from commons.utils.myLogging import get_logger

logger = get_logger()

class GetPath:
    """获取项目根目录"""

    def __str__(self):
        pass

    def getProjectRoot(self) -> str:
        """
            参数例子
            file_path = project_root.getProjectRoot() +          r"\\resources\\testdata\\soundboard"
        """

        # 当前文件路径：F:\...\commons\utils\getProjectRroot.py
        root = str(Path(__file__).parent.parent.parent.resolve())
        return root

    def getImagePath(self,template_path):
        """
        获取图片路径  template_path =          "nav4_file_voice_changer/success.png"
        :param template_path:
        :return:
        """
        # 获取当前脚本所在目录的父级（可根据项目结构调整）
        PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
        path = PROJECT_ROOT / "resources" / "images" / template_path
        return path

    def getconfiginiPath(self,filie_name):
        # 获取当前脚本所在目录的父级（可根据项目结构调整）
        PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
        path = PROJECT_ROOT / "config" / filie_name
        return path


if __name__ == '__main__':
    projectroot = GetPath()
    logger.info(projectroot.getProjectRoot())
    logger.info(projectroot.getProjectRoot()+r"\config\config.ini")
    logger.info("")
