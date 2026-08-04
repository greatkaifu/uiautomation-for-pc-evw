# 测试用例示例参考

## 断言规范

**每个测试用例必须有断言**，符合 pytest 框架语法要求。断言方式分两种：

1. **显式断言** — 使用 `assert` 语句，适用于需要判断元素是否存在、值是否正确等场景：
   - `assert result == True` — 验证元素存在
   - `assert result == False` — 验证元素不存在
   - `assert value is not None` — 验证返回值非空
   - `assert "expected" in text` — 验证文本包含

2. **隐式断言** — 使用 `control_raise`/`element_raise`，失败时抛出异常被 pytest 捕获，适用于最终验证"某元素必须存在"的场景。失败信息直接指出哪个元素不存在，比 `assert False` 更具可读性。

```python
# 显式断言：验证元素存在
result = page.find_keybind_list_item()
assert result == True

# 显式断言：验证元素不存在
result = page.find_element("nav5_voice_vreation/continue.png")
assert result == False

# 隐式断言：验证控件必须存在（推荐，失败信息更清晰）
control_raise(control, "设置页面-快捷键列表ListItem")

# 隐式断言：验证图像/图标必须存在（推荐）
element_raise("nav5_voice_vreation/continue.png", "克隆页面-上传音频后continue图片", timeout=30)
```

**禁止无断言的测试用例**：没有任何断言的 `test_*` 函数始终通过，无法检验功能正确性。

## 基本测试结构（显式断言）

```python
import allure
import pytest

from commons.utils.myLogging import get_logger
from pom.voicewave_voice_creation_page import VoicewaveVoiceCreationPage

logger = get_logger()


class TestNav5Creation:
    """
    克隆音效
    """

    @allure.story("克隆音效")
    @allure.title("进入克隆页面-Create AI voice控件正常显示")
    def test_clone_sound(self, active_window):
        """
        克隆音效
        """
        nav5_page = VoicewaveVoiceCreationPage(active_window)
        nav5_page.nav5_voice_creation()
        # 克隆页面，clone按钮控件元素，存在则点击，不存在则跳过
        try:
            clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if nav5_page.find_control(clone_btn, 3):
                nav5_page.click_clone_btn()
        except LookupError:
            pass
        # 查找 Create AI voice 控件
        create_ai_voice_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(Name='Create AI voice', ClassName='QLabel', Depth=4)
        result = nav5_page.find_control(create_ai_voice_control, 5)
        assert result == True
```

## 带 fixture 的测试用例（显式断言 + 日志）

```python
import allure
import pytest

from commons.utils.myLogging import get_logger
from pom.voicewave_setting_page import VoicewaveSettingPage

logger = get_logger()


@pytest.mark.usefixtures("active_window")
@allure.epic("PC 客户端")
@allure.feature("Settings")
class TestSettings:
    """
    Settings功能测试
    """

    @pytest.mark.test
    @allure.story("设置页-切换快捷键Tab")
    @allure.title("点击左侧栏设置，切换到快捷键Tab，验证快捷键列表存在")
    def test_switch_to_shortcuts_tab(self, active_window):
        page = VoicewaveSettingPage(active_window)
        page.click_settings_nav()
        page.allure_screenshot("点击左侧栏设置后")
        page.click_shortcuts_tab()
        page.allure_screenshot("切换到快捷键Tab后")
        result = page.find_keybind_list_item()
        if not result:
            logger.error("快捷键列表ListItem未出现")
        assert result == True
```

## 带依赖管理的测试用例

```python
@pytest.mark.dependency(name="test_clone_upload_voice")
def test_clone_upload_voice(self, active_window):
    """
    上传音频，继续克隆参数步骤，continue.png出现则用例成功
    """
    nav5_page = VoicewaveVoiceCreationPage(active_window)
    nav5_page.nav5_voice_creation()
    # 克隆页面，clone按钮控件元素，存在则点击，不存在则跳过
    try:
        clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
        if nav5_page.find_control(clone_btn, 3):
            nav5_page.click_clone_btn()
    except LookupError:
        pass
    nav5_page.click_upload_voice()
    file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
    nav5_page.input_file_path(file_path)
    nav5_page.open_file("2min.wav")
    result = nav5_page.find_element("nav5_voice_vreation/continue.png")
    assert result == True

@pytest.mark.dependency(depends=["test_clone_upload_voice"])
def test_clone_delete_voice(self, active_window):
    """
    点击delete图片删除已上传音频，continue图片不存在则用例成功
    """
    nav5_page = VoicewaveVoiceCreationPage(active_window)
    nav5_page.find_element_and_click("nav5_voice_vreation/delete.png")
    result = nav5_page.find_element("nav5_voice_vreation/continue.png")
    assert result == False
```

## 断言元素存在：control_raise/element_raise 替代 find_control/find_element + assert

当测试用例需要验证元素**必须存在**时，优先使用 `control_raise`/`element_raise` 替代 `find_control`/`find_element` + `assert`，这样失败信息直接指出哪个元素不存在：

```python
# 不推荐：失败信息只有 assert False，无法定位具体元素
result = page.find_keybind_list_item()
assert result == True

# 推荐：失败信息为 "未找到目标元素：设置页面-快捷键列表ListItem 超时 10s"
from commons.utils.targetNotFoundError import control_raise
control = self.main_window.CustomControl(...).ListItemControl(...)
control_raise(control, "设置页面-快捷键列表ListItem")

# 推荐：图像/图标断言
from commons.utils.targetNotFoundError import element_raise
element_raise("nav5_voice_vreation/continue.png", "克隆页面-上传音频后continue图片", timeout=30)
```

## 使用 control_raise / element_raise 的测试用例

```python
from commons.utils.targetNotFoundError import control_raise, element_raise

def test_clone_enter_training_page(self, active_window):
    """
    独立进入克隆页面，完整流程：上传音频 → 填信息 → 点击Create → Cancel training task控件出现
    """
    nav5_page = VoicewaveVoiceCreationPage(active_window)
    nav5_page.nav5_voice_creation()
    # 跳过CloneNowButton弹窗
    try:
        clone_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
        if nav5_page.find_control(clone_btn, 3):
            nav5_page.click_clone_btn()
    except LookupError:
        pass
    # 点击上传音频控件
    control_raise(
        active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).TextControl(ClassName='QLabel', Depth=5),
        "克隆页面-上传音频控件", timeout=5)
    nav5_page.click_upload_voice()
    file_path = project_root.getProjectRoot() + r"\resources\testdata\克隆音频"
    nav5_page.input_file_path(file_path)
    nav5_page.open_file("2min.wav")
    # 等待 continue 图片出现
    element_raise("nav5_voice_vreation/continue.png", "克隆页面-上传音频后continue图片", timeout=30)
    # 点击 Continue 按钮
    control_raise(
        active_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).CustomControl(ClassName='AnimationStackedWidget', Depth=2).GroupControl(ClassName='QScrollArea', foundIndex=1, Depth=1).ButtonControl(Name='Continue', ClassName='CustomBtn', Depth=4),
        "克隆页面-Continue按钮")
    nav5_page.click_continue_btn()
    # 输入名称
    input_control = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).EditControl(ClassName='QLineEdit', Depth=8)
    control_raise(input_control, "克隆页面-Voice名称输入框")
    nav5_page.find_control_and_input(input_control, "test123")
    # 点击 Create 按钮
    create_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Create', ClassName='CustomBtn', Depth=7)
    control_raise(create_btn, "克隆页面-Create按钮")
    nav5_page.click(create_btn)
    # 等待 Cancel training task 控件出现
    cancel_training_btn = active_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Cancel training task', ClassName='QPushButton', Depth=7)
    control_raise(cancel_training_btn, "克隆页面-Cancel training task控件", timeout=300)
```
