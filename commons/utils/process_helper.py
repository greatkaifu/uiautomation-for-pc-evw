#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : process_helper.py.py



# -*- coding: utf-8 -*-
import subprocess

from commons.utils.myLogging import get_logger

logger = get_logger()


def terminate_process(process_name: str):
    """终止指定进程（Windows）"""
    try:
        subprocess.run(["taskkill", "/F", "/IM", process_name], check=True, capture_output=True)
        logger.info(f"Terminated process: {process_name}")
    except subprocess.CalledProcessError:
        logger.warning(f"Process not found or already closed: {process_name}")


def is_process_running(process_name: str) -> bool:
    result = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
        capture_output=True, text=True
    )
    return process_name.lower() in result.stdout.lower()