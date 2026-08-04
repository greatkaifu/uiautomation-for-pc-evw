---
name: code-generator
description: 为基于 Python-UIAutomation-for-Windows 的 PC 端 UI 自动化测试项目生成符合规范的测试代码、页面对象模型（POM）和 fixtures。当用户提示到要编写自动化测试用例、创建页面类、创建测试文件、配置测试环境、"打开报告"、"查看报告"、"生成报告"时必须触发此 skill。
compatibility: 适用于 Windows 平台，依赖 uiautomation 库、pytest 和 allure-pytest
metadata:
  author: evw-team
  version: "2.0"
  project: python-uiautomation-for-pc-evw
---

# Code Generator Skill

## 概述

本项目 `python-uiautomation-for-pc-evw` 是一个基于 `Python-UIAutomation-for-Windows` 的 PC 端 UI 自动化测试框架，用于对 Windows 桌面应用程序进行自动化测试。

## 项目结构

> 完整目录树详见 [assets/project_tree.txt](assets/project_tree.txt)，以下为核心目录说明：

```
python-uiautomation-for-pc-evw/
├── bases/                      # 基础框架层
│   ├── basePage.py             # BasePage 基础页面类（所有 POM 的父类）
│   ├── captureScreen.py        # 截图工具 (ScreenElement)
│   └── mouseController.py      # 鼠标控制器 (SlowMouseController)
├── commons/utils/              # 公共工具层
│   ├── myLogging.py            # 日志 (get_logger)
│   ├── targetNotFoundError.py  # 异常 (control_raise, element_raise)
│   ├── getProjectRroot.py      # 路径 (GetPath)
│   ├── readconfig.py           # INI 读取 (INIConfigReader)
│   ├── configmanager.py        # INI 修改 (ConfigManager)
│   └── killProcess.py          # 进程 (kill_process_by_name)
├── pom/                        # 页面对象模型 (POM)
│   ├── voicewave_home_page.py  # VoiceWavePage 主页面
│   └── voicewave_*_page.py     # 各功能页面类
├── testcase/                   # 测试用例
│   └── test_*.py               # 测试文件
├── resources/
│   ├── images/                 # 图像模板（用于图像识别）
│   └── testdata/               # 测试数据文件
├── config/config.ini           # 配置文件（含安装路径）
├── conftest.py                 # pytest 共享 fixtures
├── pytest.ini                  # pytest 配置
└── requirements.txt            # 依赖
```

## 编码规范

### 1. 测试结构

- 新增测试文件时，默认在工程 `testcase/` 目录下创建，文件名格式为 `test_<feature>.py`。
- 根据测试文件名称自动生成对应的测试类名：`test_<feature>.py` → `Test<Feature>`（将下划线分隔的单词转为首字母大写的驼峰形式）。例如：`test_login.py` → `TestLogin`，`test_nav5_voice_creation.py` → `TestNav5VoiceCreation`。
- **首次创建测试文件时，只创建文件骨架（包含测试类定义和必要的 import），不要在测试类中自动添加测试用例。等用户明确告知要新增哪些测试用例后，再在测试类中添加或修改测试用例。**
- **新建测试文件时，必须同时创建对应的 POM 业务层文件**：在 `pom/` 目录下创建 `voicewave_<feature>_page.py`，类名为 `Voicewave<Feature>Page`，继承自 `BasePage`（从 `bases.basePage` 导入）。首次创建时只生成文件骨架（包含类定义和 `__init__`），类里面的方法后续根据需要再添加。参照 [templates/pom_class_template.md](templates/pom_class_template.md) 生成。**如果 `pom/` 下已存在对应的业务文件，则跳过创建，测试文件中直接 import 已有的 POM 类。**
- **新建测试文件时，必须同时在 `resources/images/` 目录下创建对应的图像目录**：目录名格式为 `<feature>_picture`，用于存放该测试文件相关的图像模板。例如：`test_login.py` → 创建 `resources/images/login_picture/`。**如果同名目录已存在，则跳过创建。**
- **新建测试文件时，必须同时在 `resources/testdata/` 目录下创建对应的测试数据目录**：目录名格式为 `<feature>_data`，用于存放该测试文件相关的测试数据文件。例如：`test_login.py` → 创建 `resources/testdata/login_data/`。**如果同名目录已存在，则跳过创建。**
- **测试类必须添加 `@allure.epic` 和 `@allure.feature` 装饰器**，参照 [templates/test_class_template.md](templates/test_class_template.md) 生成。
  - `@allure.epic` 固定为 `"PC 客户端"`。
  - `@allure.feature` 与测试类名保持一致，如 `TestLogin` → `@allure.feature("Login")`。
- 使用 `test_<scenario>` 函数命名测试方法。
- 测试类命名格式为 `Test<Feature>`。
- **上下文保持规则**：当用户新增测试用例或修改测试用例时，如果用户没有明确指定要更改的测试文件或测试类，则默认在**上一次操作的测试文件和测试类**中添加或修改测试用例。会话内首次操作若用户未指定，则需询问用户。
- 应用 `@pytest.mark.test`、`@allure.story()`、`@allure.title()` 装饰器，顺序严格为：`@pytest.mark.test` → `@allure.story` → `@allure.title`。**`@pytest.mark.dependency` 不要自动添加**，仅当用户明确要求时才添加，添加时置于 `@allure.title` 之后。
- **修改现有测试用例时**：检查是否已有 `@pytest.mark.test` —— 仅在没有时才添加，避免重复装饰。
- **每个测试用例必须有断言**：所有 `test_*` 函数必须包含至少一个符合 pytest 语法的断言，确保测试有明确的通过/失败判定。断言方式有两种：
  - **显式断言**：使用 `assert` 语句，如 `assert result == True`、`assert result == False`、`assert value is not None` 等。
  - **隐式断言**：使用 `control_raise`/`element_raise` 验证元素必须存在，失败时抛出异常被 pytest 捕获为失败。当测试步骤的最终验证是"某元素必须存在"时，优先使用此方式。
  - **禁止无断言的测试用例**：没有任何断言的测试函数始终通过，无法检验功能正确性。
- **后置清理步骤不计入断言要求**：`test_*` 函数中用于恢复环境、删除测试数据、关闭弹窗、返回上一页等 teardown/cleanup 代码不需要额外断言。断言必须放在测试的核心验证步骤上（如验证元素出现/消失、验证按钮状态、验证页面跳转结果等）。清理步骤可直接调用 POM 方法，即使失败也由抛出的异常自然反映，不强制要求 `assert` 或 `control_raise`/`element_raise`。
- **生成或修改测试用例后必须进行断言检查**：在提交最终代码前，逐行检查每个 `test_*` 函数，确认至少包含以下一种断言形式：
  - `assert` 语句
  - `control_raise(...)`
  - `element_raise(...)`
  - 其他会被 pytest 识别为失败的异常抛出
- **若发现某个 `test_*` 函数没有断言，必须立即补上**：根据测试目的，补充显式 `assert`（如 `assert result == True`）或隐式断言（如 `control_raise`/`element_raise`）。禁止直接交付无断言的测试用例。
- **使用断言检查脚本辅助验证**：生成或修改测试文件后，可运行 [scripts/check_assertions.py](scripts/check_assertions.py) 扫描 `testcase/` 目录，自动列出缺少断言的 `test_*` 函数。运行命令：
  ```bash
  python .claude/skills/code-generator/scripts/check_assertions.py testcase/
  ```
- **命名必须唯一，禁止重复**：生成或修改代码时，必须避免以下重复，重复会导致 pytest 收集用例丢失、POM 方法被覆盖或 Allure 报告混乱：
  - **测试文件名重复**：`testcase/` 目录下不能存在同名 `test_<feature>.py` 文件。
  - **测试类名重复**：同一个测试文件中不能存在同名测试类；不同文件中也应避免同名 `Test<Feature>` 类。
  - **POM 类名重复**：`pom/` 目录下不能存在同名 `Voicewave<Feature>Page` 类。
  - **POM 方法名重复**：同一个 POM 类中不能存在同名方法。
  - **测试方法名重复**：同一个测试类中不能存在同名 `test_*` 方法（后定义会覆盖前定义，导致用例丢失）。
- **生成或修改代码后必须进行重复检查**：在提交最终代码前，运行 [scripts/check_duplicates.py](scripts/check_duplicates.py) 扫描项目，自动列出重复的文件名、类名和方法名。运行命令：
  ```bash
  python .claude/skills/code-generator/scripts/check_duplicates.py
  ```
- **发现重复必须立即修复**：重命名文件、类或方法，确保命名唯一。禁止直接交付存在命名重复的代码。

- **Allure 装饰器分层规范**详见 [references/allure_decorators.md](references/allure_decorators.md)。

### 2. POM 模式 (Page Object Model)

- 页面类必须继承自 `BasePage`（从 `bases.basePage` 导入）。项目中部分旧类继承了 `VoiceWavePage`，新建 POM 类统一继承 `BasePage`，不再继承 `VoiceWavePage`。
- 通过 `super().__init__(main_window)` 实例化。
- POM 文件命名规则：`voicewave_<feature>_page.py`，类名：`Voicewave<Feature>Page`。例如：`test_first.py` → POM 文件 `voicewave_first_page.py` → 类名 `VoicewaveFirstPage`。
- **项目日志规范**：整个工程所有文件（测试文件、POM 文件等）统一使用 `from commons.utils.myLogging import get_logger` 和 `logger = get_logger()` 获取日志对象。**禁止**使用 `logging.basicConfig`、`logging.getLogger(__name__)` 或从 `bases.basePage` 导入 logger。
- **POM 方法两种模式**：根据操作是否为关键步骤，选择合适的模式。

  **模式一：关键步骤（必须成功）** — 当该步骤失败后测试无法继续时，使用 `control_raise`/`element_raise` 验证元素必须存在。失败时立即抛出异常，报错信息包含中文描述，快速定位是哪一步的哪个元素失败了。**优先使用此模式**。

```python
def click_xxx_btn(self):
    """
    点击xxx按钮
    """
    control = self.main_window.xxxControl(...)
    control_raise(control, "xxx页面-xxx按钮")
    self.click(control)
    logger.info("已点击xxx按钮。")
```

```python
def click_xxx_icon(self):
    """
    点击xxx图标
    """
    element_raise("xxx_page/xxx_icon.png", "xxx页面-xxx图标")
    self.find_element_and_click("xxx_page/xxx_icon.png")
    logger.info("已点击xxx图标。")
```

  **模式二：可选检查（可能不存在）** — 当元素可能不存在、测试需要根据结果走不同分支时，使用 `find_control`/`find_element` + try/except 日志模式，返回 `True`/`False`/`None`。

```python
def find_xxx_item(self):
    """
    查找xxx列表项
    """
    control = self.main_window.xxxControl(...)
    try:
        if self.find_control(control):
            logger.info("找到xxx列表项。")
            return True
        else:
            logger.error("未找到xxx列表项。")
            return False
    except Exception as e:
        logger.error(f"{e}")
        logger.error("未找到xxx列表项。")
        return None
```

  **选择原则**：如果后续测试步骤依赖该元素存在，用模式一；如果需要判断元素是否存在再决定后续操作，用模式二。

- 页面类模板详见 [templates/pom_class_template.md](templates/pom_class_template.md)。
- POM 完整示例详见 [references/pom_example.md](references/pom_example.md)。

### 3. Fixtures

- **模块级 (module-scoped)**：用于应用启动，在整个测试模块中只执行一次。
- **函数级 (function-scoped)**：用于每测试变体（如语言切换、用户状态切换）。
- Fixture 参考详见 [references/testcase_example.md](references/testcase_example.md)。

### 4. 元素定位策略

- **优先使用控件链**（Control Chain）：通过层级关系定位控件，提高稳定性。
- **后备方案**：图像检测（当控件属性不稳定或无法定位时）。

### 5. 图像/图标操作

- **查找并点击图像**：使用 `self.find_element_and_click(template_path, timeout=None)`，禁止手写图像检测 + 点击逻辑。timeout=None即不等待只查找一次，设置timeout后会在超时时间内轮询等待元素出现。
- **检查图像/图标是否存在**：使用 `self.find_element(template_path, timeout=None)`，找到返回 `True`，未找到返回 `False`。timeout=None则使用类里面默认的超时。
- **查找图像/图标并输入内容**：使用 `self.find_element_and_input(template_path, content, timeout=None)`，timeout=None即不等待只查找一次。
- **图像/图标必须存在时的异常处理**：使用 `element_raise(template_path, description, timeout)`（来自 `commons.utils.targetNotFoundError`）。
- **相对图像点击**：使用 `self.click_relative_to_element(template_path, offset_x, offset_y, timeout=None)`，timeout=None即不等待只查找一次。
- **鼠标悬停到图像位置**：使用 `self.hover_to_element(template_path, timeout=None)`，不存在时抛 `TargetElementNotFoundError`。
- **相对图像偏移位置发送内容**：使用 `self.send_to_contents(template_path, str_content, offset_x, offset_y, timeout=None)`，不存在时抛 `TargetElementNotFoundError`。
- **通过滚动查找图像/图标**：使用 `self.find_element_by_scroll_up_and_down(template_path, max_scroll_down, max_scroll_up)`，通过滚轮上下滚动查找图像或图标，找到返回 `True`，未找到返回 `None`。
- **通过单向滚动查找图像/图标**：使用 `self.find_element_by_scroll(template_path, max_scroll_count, scroll_direction, scroll_interval)`，单方向（上或下）滚动查找图像或图标，找到返回 `True`，未找到返回 `None`。

### 6. UI 控件操作

- **点击控件**：`self.click(control, timeout, move_duration, press_duration, move_steps)`
- **双击控件**：`self.double_click(control, timeout, interval)`
- **检查控件是否存在**：`self.find_control(control, timeout)`，找到返回 `True`，未找到返回 `False`。
- **查找控件并输入内容**：`self.find_control_and_input(input_control, content, timeout, clear)`，`clear=True` 时先清空原有内容。
- **通过滚动查找控件**：`self.find_control_by_scroll_up_and_down(control, max_scroll_down, max_scroll_up, scroll_interval, scroll_amount)`，通过滚轮上下滚动查找 UI 控件，找到返回 `True`，未找到返回 `False`。
- **控件必须存在时的异常处理**：使用 `control_raise(control, description, timeout)`（来自 `commons.utils.targetNotFoundError`）。

完整 API 速查详见 [references/api_reference.md](references/api_reference.md)。

### 7. 等待操作

- **等待图像出现**：使用 `self.wait_for_image_appear(image_path, timeout=30)`，在规定时间内循环等待图像出现，出现返回 `True`，超时返回 `False`。
- **等待图像消失**：使用 `self.wait_for_image_disappear(image_path, timeout=10)`，在规定时间内循环等待图像消失，消失返回 `True`，超时返回 `False`。
- **等待控件出现**：使用 `self.wait_for_control_appear(control, timeout=600)`，循环等待控件出现，出现返回 `True`，超时返回 `False`。
- **等待控件消失**：使用 `self.wait_for_control_disappear(control, timeout=30)`，循环等待控件消失，消失返回 `True`，超时返回 `False`。

### 8. 键盘/剪贴板操作

- **输入字符**：使用 `self.send_contents(str_content)`，发送字符内容。
- **回车键**：使用 `self.enter()`，输入回车键。
- **全选**：使用 `self.selectAll()`，`{Ctrl}{A}`。
- **删除**：使用 `self.delete()`，`{Delete}`。
- **复制**：使用 `self.copy()`，`{Ctrl}{C}`。
- **粘贴**：使用 `self.paste()`，`{Ctrl}{V}`。
- **输出剪贴板**：使用 `self.clip_output()`，返回剪贴板文本内容。
- **发送按键组合**：使用 `self.send_keys(keys, wait_time=0.5)`，发送键盘按键组合（如 `'{Ctrl}{A}'`）。
- **直接点击坐标**：使用 `self.click_coord(x, y, wait_time=0.5)`，直接点击屏幕坐标。
- **移动到坐标**：使用 `self.move_to(x, y, wait_time=0.5)`，移动鼠标到指定坐标。
- **相对鼠标位置点击**：使用 `self.click_mouse_relative_positon(offset_x=0, offset_y=0)`，相对当前鼠标位置偏移点击。
- **查找控件后相对鼠标点击**：使用 `self.find_control_and_click_relative_cursor(control, offset_x=0, offset_y=0, timeout=None, description='')`，先查找控件，再相对鼠标位置偏移点击。

### 9. Allure 报告截图

- **操作步骤截图**：使用 `self.allure_screenshot(name)` 截取当前屏幕并附加到 Allure 报告，参数 `name` 为步骤描述（如 "点击设置后"）。该方法为静态方法，但在测试用例中通过页面对象实例调用即可（如 `page.allure_screenshot("描述")`），无需在 POM 方法内部调用。
- **调用位置**：在测试用例中，通过页面对象实例调用（如 `page.allure_screenshot("描述")`），而非在 POM 方法内部调用。
- **使用时机**：在关键操作步骤之后调用，每个关键操作都应截图记录，便于失败时定位问题。
- **滚动查找时的截图规则**：当测试用例中使用了滚动查找控件（`find_control_by_scroll_up_and_down`）或滚动查找图像/图标（`find_element_by_scroll_up_and_down`）时，截图必须放在滚动查找完成之后（找到或未找到时），不要在滚动查找之前截图。这样截图才能记录滚动的最终结果状态。示例：

```text
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
    assert result == True

@pytest.mark.test
@allure.story("设置页-General页滚动查找")
@allure.title("进入设置General页，滚动查找圆点图片")
def test_general_scroll_dot(self, active_window):
    page = VoicewaveSettingPage(active_window)
    page.click_settings_nav()
    page.allure_screenshot("点击左侧栏设置后")
    page.click_general_tab_btn()
    page.click_general_page_label()
    # 滚动查找，截图在查找完成后而非之前
    result = page.find_dot_by_scroll()
    page.allure_screenshot("滚动查找圆点后")
    assert result == True
```

### 10. 异常处理策略

- **关键步骤必须使用 `control_raise`/`element_raise`**：在 POM 业务方法和测试用例中，凡是后续操作依赖元素存在的步骤，都必须使用 `control_raise`（UI 控件）或 `element_raise`（图像/图标）验证元素存在。
- **使用场景**：
  - POM 方法中：关键操作前用 `control_raise`/`element_raise` 验证，确保失败时异常信息包含中文描述（如 `"设置页面-快捷键Tab按钮"`），快速定位失败步骤和元素。
  - 测试用例中：断言元素必须存在时，用 `control_raise`/`element_raise` 替代 `find_control` + `assert True`，这样失败信息直接指出哪个元素不存在，而不是模糊的 `assert False`。
- **导入方式**：`from commons.utils.targetNotFoundError import control_raise, element_raise`
- **description 命名规范**：`"<页面>-<元素描述>"`，如 `"设置页面-快捷键Tab按钮"`、`"克隆页面-上传音频控件"`，便于在报错中一眼定位。
- **可选检查场景**：仅在元素可能不存在、测试需要根据结果走不同分支时，使用 `find_control`/`find_element` 返回布尔值。
- 参考实现详见 [references/targetNotFoundError.py](references/targetNotFoundError.py)。

### 11. 文件管理器操作

- **输入文件路径**：使用 `self.input_file_path(file_path)`。
- **打开文件**：使用 `self.open_file(filename)`。

### 12. 配置管理

- 使用 `GetPath()` 获取项目路径。
- 使用 `ConfigManager` 管理配置项（如环境配置、超时时间等）。

#### 自动配置安装路径规则

当用户提示中包含 **"配置"** 或 **"配置安装路径"** 时：
- 如果用户提供的信息中包含 `.exe` 路径，则**必须**将该路径写入 `config.ini` 文件的 `[install]` 节下的 `path` 配置项，覆盖原有 `path` 值（保留注释行不变）。
- 仅当路径以 `.exe` 结尾时才执行此自动配置操作。

#### 用户仅提供 Name 等属性值的情况

如果用户只提供了属性值（如只给了 Name）：
- 仅修改 `auto.WindowControl(...)` 的对应参数。
- 同时修改 `print("正在启动 EaseUS VoiceWave...")` 的输出内容，使用新的 `WindowControl` 的 `Name` 属性值。
- **只修改 `active_mainwin()` 这一个 fixture**，不要修改 `conftest.py` 中其他 fixture。

## 注意事项

1. **图像模板路径**：统一放在 `resources/images/` 目录下，使用 `GetPath().getImagePath()` 获取完整路径。
2. **超时处理**：所有查找/点击操作都应设置合理的超时时间，避免测试卡死。使用 `auto.WaitForExist(control, timeout)` 代替 `time.sleep()`。
3. **异常处理与断言**：对必须存在的元素使用 `element_raise` 或 `control_raise`，确保失败时有清晰的中文报错信息。每个测试用例必须有至少一个断言（显式 `assert` 或隐式 `control_raise`/`element_raise`），禁止无断言的测试用例。
4. **控件链稳定性**：控件链定位依赖应用 UI 层级结构，UI 改版时需同步更新页面类。
5. **图像检测限制**：图像检测受分辨率、缩放比例、主题颜色影响，仅作为后备方案。
6. **测试执行过滤规则**：当用户提示词中包含 **"调试"** 或 **"执行"** 时，**只执行带有 `@pytest.mark.test` 标记的测试用例**，执行命令中必须包含 `-m test` 参数。
7. **Allure 报告规则**：当用户提示词中包含 **"生成报告"**、**"打开报告"** 或 **"查看报告"** 时，必须严格按 [scripts/run_commands.md](scripts/run_commands.md) 中的流程执行。核心流程：先检查 `allure-results/` 是否存在且非空 → 有数据则直接生成报告 → 无数据则先执行测试用例生成数据再生成报告 → 最后通过 `allure open report` 启动本地 HTTP 服务器打开报告。**禁止直接用浏览器打开 `report/index.html`**，必须通过 `allure open report` 启动本地 HTTP 服务器来打开报告。
8. **全量测试执行规则**：当用户提示词中包含 **"执行所有"** 或 **"执行所有用例"** 时，执行 `testcase/` 目录下所有测试文件。

## Assets 参考资源

以下文件位于 `assets/` 目录，提供真实的项目源码和结构快照，生成代码时必须参照：

| 文件 | 用途 |
|------|------|
| [project_tree.txt](assets/project_tree.txt) | 真实项目目录结构与路径映射，替代上方精简版结构 |
| [basepage_api_full.py](assets/basepage_api_full.py) | BasePage 完整源码，包含所有方法签名、参数、返回值 |
| [captureScreen_api_full.py](assets/captureScreen_api_full.py) | ScreenElement 完整源码，包含所有方法签名、参数、返回值 |
| [conftest_fixture_snapshot.py](assets/conftest_fixture_snapshot.py) | 所有可用 fixture 的签名、scope、返回值、选择指南 |
| [existing_pom_examples/](assets/existing_pom_examples/) | 真实 POM 页面类完整源码，学习 import 风格、日志模式、异常处理 |
| [existing_test_examples/](assets/existing_test_examples/) | 真实测试文件完整源码，学习 fixture 用法、allure 装饰器、断言模式、截图调用 |
