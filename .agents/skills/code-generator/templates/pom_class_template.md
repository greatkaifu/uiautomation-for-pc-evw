# POM 页面类模板

新建 POM 页面类时，按以下模板生成代码，将 `{{feature}}` 和 `{{Feature}}` 替换为实际值：

- `{{feature}}` → 小写下划线形式，如 `login`、`nav5_voice_creation`
- `{{Feature}}` → 首字母大写驼峰形式，如 `Login`、`Nav5VoiceCreation`
- `{{FeatureDescription}}` → 功能描述，如 `登录页面`

```text
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : leikaifu
# @File    : voicewave_{{feature}}_page.py
# @IDE     : PyCharm
from bases.basePage import BasePage
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import control_raise, element_raise
import uiautomation

logger = get_logger()


class Voicewave{{Feature}}Page(BasePage):
    """
        {{FeatureDescription}}
    """

    def __init__(self, main_window):
        super().__init__(main_window)
```