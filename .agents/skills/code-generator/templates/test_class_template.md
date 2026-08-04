# 测试类模板

新建测试文件时，按以下模板生成代码，将 `{{feature}}` 和 `{{Feature}}` 替换为实际值：

- `{{feature}}` → 小写下划线形式，如 `login`、`nav5_voice_creation`
- `{{Feature}}` → 首字母大写驼峰形式，如 `Login`、`Nav5VoiceCreation`

```text
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
import allure
import pytest

from commons.utils.myLogging import get_logger
from pom.voicewave_{{feature}}_page import Voicewave{{Feature}}Page

logger = get_logger()


@allure.epic("PC 客户端")
@allure.feature("{{Feature}}")
class Test{{Feature}}:
    """
    {{Feature}}功能测试
    """
    pass
```

### 测试方法装饰器顺序

```text
@pytest.mark.test
@allure.story("...")
@allure.title("...")
def test_<scenario>(self, ...):
```

> **注意**：`@pytest.mark.dependency` 不要自动添加，仅当用户明确要求时才添加，添加时置于 `@allure.title` 之后。

### 测试方法断言要求

每个测试方法必须有至少一个断言，确保测试有明确的通过/失败判定：

- **显式断言**：使用 `assert` 语句（如 `assert result == True`、`assert result == False`）
- **隐式断言**：使用 `control_raise`/`element_raise` 验证元素必须存在，失败时抛出异常被 pytest 捕获

禁止无断言的测试方法。