#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : leikaifu
# @File    : voicewave_voice_page.py
# @IDE     : PyCharm
from bases.basePage import BasePage
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import control_raise, element_raise
import uiautomation

logger = get_logger()


class VoicewaveVoicePage(BasePage):
    """
       Voice页面
    """

    def __init__(self, main_window):
        super().__init__(main_window)
