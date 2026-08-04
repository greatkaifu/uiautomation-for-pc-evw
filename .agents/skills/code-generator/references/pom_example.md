# POM 页面类示例参考

## 基本结构

页面类继承 `BasePage`，通过 `super().__init__(main_window)` 实例化

```python
from bases.basePage import BasePage
import uiautomation as auto

class LoginPage(BasePage):
    def __init__(self, main_window):
        super().__init__(main_window)

    def login(self, username, password):
        """登录操作封装"""
        control = self.main_window.EditControl(Name="用户名")
        self.find_control_and_input(control, username)
        control = self.main_window.EditControl(Name="密码")
        self.find_control_and_input(control, password)
        self.click(self.main_window.ButtonControl(Name="登录"))
```

## 关键步骤模式（推荐）：使用 control_raise / element_raise

当操作为关键步骤（后续步骤依赖该元素存在）时，使用 `control_raise`/`element_raise` 验证元素必须存在。失败时抛出异常，报错信息包含中文描述，快速定位失败步骤和元素。

```python
from bases.basePage import BasePage
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import control_raise, element_raise

logger = get_logger()


class VoicewaveSettingPage(BasePage):
    """
    Setting页面操作封装
    """

    def __init__(self, main_window):
        super().__init__(main_window)

    def click_settings_nav(self):
        """
        点击左侧栏设置功能控件
        """
        control = self.main_window.GroupControl(ClassName='PageSelWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.widget_Sel', Depth=4).ListControl(ClassName='CNaviListWidget', Depth=1).ListItemControl(foundIndex=6, Depth=1)
        control_raise(control, "设置页面-左侧栏设置功能控件")
        self.click(control)
        logger.info("已点击左侧栏设置功能控件。")

    def click_shortcuts_tab(self):
        """
        在Setting页，点击快捷键TabButton
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='SettingWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.SettingWidget', Depth=1).GroupControl(ClassName='TabsWidget', Depth=1).GroupControl(ClassName='QScrollArea', Depth=1).ButtonControl(ClassName='TabButton', foundIndex=2, Depth=3)
        control_raise(control, "设置页面-快捷键Tab按钮")
        self.click(control)
        logger.info("已点击快捷键TabButton。")

    def click_upload_icon(self):
        """
        点击上传图标
        """
        element_raise("nav3_community_library/upload_button.png", "社区音效页-上传按钮图标")
        self.find_element_and_click("nav3_community_library/upload_button.png", timeout=10)
        logger.info("已点击上传按钮图标。")
```

## 可选检查模式：find_control + try/except 日志

当元素可能不存在、测试需要根据结果走不同分支时，使用 `find_control`/`find_element` + try/except 日志模式。

```python
from bases.basePage import BasePage
from commons.utils.myLogging import get_logger

logger = get_logger()


class VoicewaveSettingPage(BasePage):
    """
    Setting页面操作封装
    """

    def __init__(self, main_window):
        super().__init__(main_window)

    def find_keybind_list_item(self):
        """
        在快捷键页，查找快捷键列表ListItem控件
        :return: True 找到控件，False 未找到
        """
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='QStackedWidget', Depth=2).ListItemControl(Depth=5)
        result = self.find_control(control)
        return result

    def find_dot_by_scroll(self):
        """
        在General页，通过滚轮查找圆点图片
        :return: True 找到图片，None 未找到
        """
        result = self.find_element_by_scroll_up_and_down('nav6_settings/圆点.png', max_scroll_down=50, max_scroll_up=50)
        logger.info(f"滚动查找圆点图片结果: {result}")
        return result

    def dismiss_upgrade_popup(self):
        """
        关闭升级弹窗（弹窗可能不出现）
        :return: True 成功关闭，False 弹窗未出现
        """
        try:
            if self.find_element("common/close_upgrade_popup.png", timeout=3):
                self.find_element_and_click("common/close_upgrade_popup.png")
                logger.info("已关闭升级弹窗。")
                return True
            else:
                logger.info("升级弹窗未出现，跳过。")
                return False
        except Exception as e:
            logger.error(f"{e}")
            logger.error("关闭升级弹窗异常。")
            return None
```

## 混合使用示例

同一个页面类中，关键步骤用 `control_raise`/`element_raise`，可选检查用 `find_control`/`find_element`。

```python
from bases.basePage import BasePage
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import control_raise, element_raise

logger = get_logger()


class VoicewaveVoiceCreationPage(BasePage):
    """
    音色克隆页面操作封装
    """

    def __init__(self, main_window):
        super().__init__(main_window)

    def nav5_voice_creation(self):
        """
        导航到音色克隆页面
        """
        control = self.main_window.GroupControl(ClassName='PageSelWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.widget_Sel', Depth=4).ListControl(ClassName='CNaviListWidget', Depth=1).ListItemControl(foundIndex=5, Depth=1)
        control_raise(control, "音色克隆页面-左侧栏导航控件")
        self.click(control)
        logger.info("已导航到音色克隆页面。")

    def click_clone_btn(self):
        """
        点击Clone Now按钮（关键步骤，必须成功）
        """
        clone_btn = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
        control_raise(clone_btn, "音色克隆页面-Clone Now按钮")
        self.click(clone_btn)
        logger.info("已点击Clone Now按钮。")

    def find_continue_image(self):
        """
        查找continue图片（可选检查，上传后可能出现）
        :return: True 找到，False 未找到
        """
        result = self.find_element("nav5_voice_vreation/continue.png", timeout=30)
        return result

    def skip_clone_popup(self):
        """
        跳过Clone弹窗（弹窗可能不出现）
        :return: True 成功跳过，False 无弹窗
        """
        try:
            clone_btn = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(ClassName='CloneNowButton', Depth=8)
            if self.find_control(clone_btn, 3):
                self.click(clone_btn)
                logger.info("已跳过Clone弹窗。")
                return True
            return False
        except Exception as e:
            logger.error(f"{e}")
            return False
```

## 图像识别操作示例（关键步骤模式）

```python
from bases.basePage import BasePage
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import element_raise

logger = get_logger()


class VoicewaveCommunityPage(BasePage):
    """
    VoicewaveCommunityPage 社区音效页操作封装
    """

    def __init__(self, main_window):
        super().__init__(main_window)

    def click_uploadsounds_button(self):
        """
        在community页，点击uploadsounds按钮（图像识别方式，关键步骤）
        """
        element_raise("nav3_community_library/upload_button.png", "社区音效页-uploadsounds按钮图标")
        self.find_element_and_click("nav3_community_library/upload_button.png")
        logger.info("已点击uploadsounds按钮。")

    def close_uploadsounds_alert(self):
        """
        在社区音效页，关闭uploadsounds弹窗（关键步骤）
        """
        control = self.main_window.GroupControl(ClassName='SBWebUploadWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)
        control_raise(control, "社区音效页-uploadsounds弹窗关闭按钮")
        self.click(control)
        logger.info("已关闭uploadsounds弹窗。")
```
