#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : basePage.py
import os
import tempfile

import allure
import pyautogui
import pyperclip
import uiautomation
import uiautomation as auto
from ctypes import wintypes
import time
from pathlib import Path
import wmi
import ctypes

# Windows API 常量定义
from bases.captureScreen import ScreenElement
from bases.mouseController import SlowMouseController
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger
from commons.utils.targetNotFoundError import TargetControlNotFoundError, TargetElementNotFoundError, control_raise

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
SM_CXSCREEN = 0
SM_CYSCREEN = 1

# 配置日志
logger = get_logger()

# 项目根目录类
project_root = GetPath()


class BasePage():
    """
    基于 uiautomation 的pc客户端 UI 自动化基类
    """

    """UI自动化操作封装类"""

    def __init__(self, main_window, default_timeout=10,
                 slow_move_duration=0.8,
                 slow_press_duration=0.3,
                 slow_move_steps=45):
        """
        初始化UI自动化封装器

        :param default_timeout: 默认控件等待超时时间（秒）
        :param slow_move_duration: 缓慢移动鼠标总时长（秒）
        :param slow_press_duration: 鼠标按下后保持时长（秒）
        :param slow_move_steps: 移动过程分步数（值越大轨迹越平滑）
        """
        self.main_window = main_window
        self.default_timeout = default_timeout
        self.slow_move_duration = slow_move_duration
        self.slow_press_duration = slow_press_duration
        self.slow_move_steps = slow_move_steps

        # 获取屏幕分辨率
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        # 激活窗口（确保在前台）
        if not isinstance(main_window, auto.Control):
            raise TypeError("window_name 必须是 uiautomation.Control 类型")
        try:
            #  用 Windows API 将窗口置顶，确保后续鼠标/键盘操作作用于该窗口
            # self.main_window.SetTopmost(True)
            # 激活窗口，确保后续鼠标/键盘操作作用于该窗口
            self.main_window.SetActive()
            time.sleep(0.5)
            logger.info(f"窗口已激活: {self.main_window}")
        except Exception as e:
            logger.info(f"异常: {e}")

    def _is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    def _select_file(self, file_name):
        """
        在文件管理器页，选择不同的格式文件

        """
        if file_name == "sample.aac" or file_name == "sample.ac3" or file_name == "sample.mp2":
            control = self.main_window.ComboBoxControl(Name='文件类型(T):', ClassName='ComboBox', Depth=2)
            BasePage.click(self, control, timeout=2)
            element = ScreenElement(GetPath().getImagePath("nav4_file_voice_changer/file1.png"))
            element.click(delay=1)

        # 文件空间元素地址
        file_name_control = self.main_window.PaneControl(Name='文件夹布局窗格', ClassName='Element', Depth=4).PaneControl(
            Name='Shell 文件夹视图', ClassName='DUIListView', Depth=1).ListItemControl(Name=file_name, ClassName='UIItem',
                                                                                  Depth=2).EditControl(Name='名称',
                                                                                                       ClassName='UIProperty',
                                                                                                       Depth=1)
        if auto.WaitForExist(file_name_control, 5):
            BasePage.click(self, file_name_control)
        else:
            logger.warning("[警告] 未找到文件，请检查文件名。")

    def _get_cursor_position(self):
        """获取当前鼠标坐标"""
        point = wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y

    def _to_int(self, value):
        """将 ctypes 类型转换为 Python int"""
        return int(value.value) if hasattr(value, 'value') else int(value)

    def _smooth_move_to(self, target_x, target_y, duration=None, steps=None):
        """
        平滑移动鼠标到目标坐标

        :param target_x: 目标X坐标（屏幕绝对坐标）
        :param target_y: 目标Y坐标（屏幕绝对坐标）
        :param duration: 移动总时长（秒），None时使用实例默认值
        :param steps: 移动分步数，None时使用实例默认值
        """
        duration = duration if duration is not None else self.slow_move_duration
        steps = steps if steps is not None else self.slow_move_steps

        if steps <= 0 or duration <= 0:
            ctypes.windll.user32.SetCursorPos(target_x, target_y)
            return

        # 使用转换函数
        start_x, start_y = self._get_cursor_position()

        start_x = self._to_int(start_x)
        start_y = self._to_int(start_y)
        target_x = self._to_int(target_x)
        target_y = self._to_int(target_y)

        # 起始位置与目标位置相同则跳过移动
        if start_x == target_x and start_y == target_y:
            return

        # 计算每步增量和延迟
        step_x = (target_x - start_x) / steps
        step_y = (target_y - start_y) / steps
        delay_per_step = duration / steps

        # 逐步移动鼠标
        for i in range(1, steps + 1):
            current_x = int(start_x + step_x * i)
            current_y = int(start_y + step_y * i)
            ctypes.windll.user32.SetCursorPos(current_x, current_y)
            time.sleep(delay_per_step)

    def _mouse_left_down(self):
        """模拟鼠标左键按下"""
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN

    def _mouse_left_up(self):
        """模拟鼠标左键释放"""
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP

    def click(self, control, timeout=None,
              move_duration=None, press_duration=None, move_steps=None):
        """
        缓慢点击控件（含平滑移动+缓慢按下/释放）

        :param control: uiautomation.Control 对象
        :param timeout: 等待控件出现的超时时间（秒）
        :param move_duration: 鼠标移动到控件的时长（秒），None时使用实例默认值
        :param press_duration: 鼠标按下后保持的时长（秒），None时使用实例默认值
        :param move_steps: 移动分步数，None时使用实例默认值
        :return: bool - 是否点击成功
        """
        if not isinstance(control, auto.Control):
            logger.error("slow_click() 传入的 control 不是有效的 Control 对象")
            return False

        timeout = timeout if timeout is not None else self.default_timeout
        press_duration = press_duration if press_duration is not None else self.slow_press_duration

        try:
            # 等待控件出现
            if not auto.WaitForExist(control, timeout):
                logger.warning(f"控件在 {timeout} 秒内未出现，无法执行缓慢点击")
                return False

            # 获取控件中心坐标
            rect = control.BoundingRectangle
            if not rect:
                logger.error("无法获取控件坐标，BoundingRectangle 为空")
                return False

            center_x = int(rect.left + rect.width() / 2)
            center_y = int(rect.top + rect.height() / 2)

            # 步骤1: 平滑移动鼠标到控件中心
            logger.debug(f"开始平滑移动鼠标到控件中心: ({center_x}, {center_y})")
            self._smooth_move_to(center_x, center_y, duration=move_duration, steps=move_steps)
            time.sleep(0.05)  # 短暂稳定鼠标位置

            # 步骤2: 缓慢按下鼠标左键
            logger.debug("执行鼠标左键按下操作")
            self._mouse_left_down()
            time.sleep(press_duration)  # 保持按下状态

            # 步骤3: 缓慢释放鼠标左键
            logger.debug("执行鼠标左键释放操作")
            self._mouse_left_up()
            time.sleep(0.1)  # 点击后短暂延迟确保操作生效

            # 记录成功日志
            try:
                control_name = control.Name or 'N/A'
            except Exception:
                control_name = 'Unavailable'
            try:
                class_name = control.ClassName or 'N/A'
            except Exception:
                class_name = 'Unavailable'

            logger.info(
                f"成功执行缓慢点击: Name={control_name}, "
                f"ClassName={class_name}, "
                f"Position=({center_x},{center_y}), "
                f"MoveDuration={move_duration or self.slow_move_duration}s, "
                f"PressDuration={press_duration}s"
            )
            return True

        except Exception as e:
            logger.error(f"缓慢点击控件时发生异常: {e}")
            # 确保异常时释放鼠标按键
            try:
                self._mouse_left_up()
            except:
                pass
            return False

    def double_click(self, control, timeout=None, interval=0.1, **kwargs):
        """
        缓慢双击控件

        :param control: uiautomation.Control 对象
        :param timeout: 等待控件超时时间
        :param interval: 两次点击间隔时间（秒）
        :param kwargs: 传递给 slow_click 的参数（move_duration, press_duration 等）
        :return: bool - 是否双击成功
        """
        if self.click(control, timeout=timeout, **kwargs):
            time.sleep(interval)
            return self.click(control, timeout=timeout, move_duration=0.2, **kwargs)
        return False

    def find_control_text(self, control, timeout=None):
        """
        根据控件名称查找控件Name属性值

        :param control_name: 控件名称
        :param timeout: 超时（秒），若为 None 则使用 self.default_timeout
        :return: uiautomation.Control - 找到的控件对象返回Name属性值，若未找到则返回 None
        """
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout
        try:
            # 等待按钮出现
            if auto.WaitForExist(control, timeout):
                Name = control.Name
                logger.info(f"控件元素已经找到，Name属性值为: {Name}")
                return Name
        except Exception as e:
            logger.error(f"查找控件时发生异常: {e}")
            return None

    def find_control(self, control, timeout=None):
        """
        根据控件名称查找控件位置

        :param control_name: 控件名称
        :param timeout: 超时（秒），若为 None 则使用 self.default_timeout
        :return: uiautomation.Control - 找到的控件对象，若未找到则返回 None
        """
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout
        try:
            # 等待按钮出现
            if auto.WaitForExist(control, timeout):
                logger.info(f"控件已经找到: {control}")
                return True
        except Exception as e:
            logger.error(f"查找{ control}控件时发生异常: {e}")
            return False

    def find_control_and_input(self, input_control, content, timeout=None, clear=False):
        """
        查找控件并输入内容

        :param input_control: uiautomation.Control 控件对象
        :param content: 要输入的内容
        :param timeout: 等待控件出现的超时时间（秒），若为 None 则使用 self.default_timeout
        :param clear: 是否在输入前清空控件内容，默认 False
        :return: bool - 输入成功返回 True，失败返回 False
        """
        timeout = timeout if timeout is not None else self.default_timeout
        try:
            if not auto.WaitForExist(input_control, timeout):
                logger.warning(f"控件在 {timeout} 秒内未出现，无法输入内容")
                return False

            # 点击控件获取焦点
            self.click(input_control, timeout=1, move_duration=0.3, press_duration=0.1)
            time.sleep(0.2)

            # 如需清空，先全选再删除
            if clear:
                self.selectAll()
                self.delete()
                time.sleep(0.1)

            # 输入内容
            auto.SendKeys(content, waitTime=0.3)
            logger.info(f"已在控件中输入内容: {content}")
            return True

        except Exception as e:
            logger.error(f"查找控件并输入内容时发生异常: {e}")
            return False

    def toggle_network_wmi(self, adapter_name, enable=True):
        """
        通过 WMI 启用或禁用网络适配器
        调用方式       toggle_network_wmi("以太网", enable=True)
        :param adapter_name: 适配器名称
        :param enable: 是否启用，默认为 True
        :return: None
        """

        if not self._is_admin():
            logger.error("[ERROR] 需要管理员权限")
            return

        c = wmi.WMI()
        adapters = c.Win32_NetworkAdapter(NetConnectionID=adapter_name)

        if not adapters:
            logger.error(f"[ERROR] 未找到适配器：{adapter_name}")
            return

        for adapter in adapters:
            try:
                if enable:
                    adapter.Enable()
                    logger.info(f"[SUCCESS] 已启用：{adapter.NetConnectionID}")
                else:
                    adapter.Disable()
                    logger.info(f"[SUCCESS] 已禁用：{adapter.NetConnectionID}")
            except Exception as e:
                logger.error(f"[ERROR] 操作失败：{e}")

    def check_flie_and_delete(self, file_path, file_style):
        """
        在指定目录下查找唯一的指定类型文件并删除（忽略大小写）

        参数:
            file_path (str): 文件路径或目录路径
            file_style (str): 文件扩展名（如 '.mp4' 或 'mp4'，不区分大小写）

        返回:
            bool: 删除成功返回 True，否则返回 False
        """

        # 1. 标准化扩展名：转小写并确保以 '.' 开头
        if not file_style.startswith('.'):
            file_style = '.' + file_style
        file_style = file_style.lower()  # 转为小写，实现忽略大小写

        # 2. 确定目录路径
        if os.path.isfile(file_path):
            dir_path = os.path.dirname(file_path)
        elif os.path.isdir(file_path):
            dir_path = file_path
        else:
            dir_path = os.path.dirname(file_path)

        # 3. 检查目录是否存在
        if not os.path.isdir(dir_path):
            return False

        # 4. 查找目录下所有匹配的文件（忽略大小写）
        matched_files = []
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(file_style):
                matched_files.append(filename)

        # 5. 前提：目录下只有一个匹配的文件
        if len(matched_files) != 1:
            return False

        # 6. 构建完整文件路径并删除
        full_path = os.path.join(dir_path, matched_files[0])
        try:
            os.remove(full_path)
            return True
        except (OSError, PermissionError):
            return False

    def clear_directory(self, dir_path):
        """
        删除指定目录下的所有文件（不包含子文件夹）
        :param dir_path: 目录路径
        :return: 成功删除的文件数量
        """
        path = Path(dir_path)
        deleted_count = 0

        if not path.exists():
            logger.warning(f"目录不存在：{path}")
            return 0

        if not path.is_dir():
            logger.error(f"路径不是目录：{path}")
            return 0

        try:
            for item in path.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                        deleted_count += 1
                        logger.info(f"已删除：{item.name}")
                    elif item.is_dir():
                        logger.info(f"跳过文件夹：{item.name}")
                except PermissionError:
                    logger.error(f"权限不足，无法删除：{item.name}")
                except Exception as e:
                    logger.error(f"删除失败 {item.name}: {e}")

            logger.info(f"清理完成，共删除 {deleted_count} 个文件")
            return deleted_count

        except Exception as e:
            logger.error(f"遍历目录时出错：{e}")
            return 0

    def find_element_by_scroll(self, template_path, max_scroll_count=5, scroll_direction='down', scroll_interval=1.0):
        """
        查找控件，如果找不到则执行滚轮滚动，直到找到或达到最大滚动次数。
        :param template_path: 模版路径地址
        :param max_scroll_count: 最大滚动次数 (参数控制)
        :param scroll_direction: 滚动方向 ('up' 或 'down')
        :param scroll_interval: 每次滚动后的等待时间 (秒)，给 UI 渲染留时间
        :return: 找到返回 True，未找到返回 None
        """
        logger.info(f"开始查找控件，最大尝试滚动：{max_scroll_count} 次")
        # 拼接完整图片路径（字符串）
        element = ScreenElement(project_root.getImagePath(template_path))
        for i in range(max_scroll_count + 1):
            # 2. 尝试查找控件
            try:

                # 通过匹配查找图片坐标位置
                if element.find():
                    logger.info(f"控件已经找到坐标位置: {element.find()}")
                    logger.info(f"在第 {i + 1} 次查找时成功找到控件！")
                    return True
                logger.info(f"第 {i + 1} 次查找未找到，准备执行滚动... (剩余次数：{max_scroll_count - i})")
            except Exception as e:
                logger.error(f"查找控件时发生异常: {e}")
                return False

            # 3. 如果还没达到最大次数，执行滚动
            if i < max_scroll_count:
                # 确定滚动数值 (pyautogui: 正数向上，负数向下)
                scroll_amount = 1  # 每次滚动的刻度数
                if scroll_direction == 'down':
                    scroll_amount = -scroll_amount
                elif scroll_direction == 'up':
                    scroll_amount = scroll_amount
                else:
                    scroll_amount = -1
                    logger.info("方向参数错误，默认为向下")

                # 执行滚轮事件
                pyautogui.scroll(scroll_amount)

                # 4. 等待 UI 加载/渲染
                time.sleep(scroll_interval)
            else:
                logger.error("已达到最大滚动次数，仍未找到控件。")

        return None

    def find_control_by_scroll_up_and_down(self, control, max_scroll_down=20, max_scroll_up=20, scroll_interval=0.5, scroll_amount=1):
        """
        通过滚轮上下滚动查找控件，找到即停止
        :param control: uiautomation.Control 控件对象
        :param max_scroll_down: 最大向下滚动次数
        :param max_scroll_up: 最大向上滚动次数
        :param scroll_interval: 每次滚动后的等待时间（秒）
        :param scroll_amount: 每次滚动的格数，值越大滚动幅度越大
        :return: True 找到控件，False 未找到
        """
        # 先不滚动，直接检查
        if control.Exists(0):
            logger.info(f"未滚动即找到控件: {control}")
            return True

        # 向下滚动查找
        for i in range(max_scroll_down):
            pyautogui.scroll(-scroll_amount)
            time.sleep(scroll_interval)
            if control.Exists(0):
                logger.info(f"向下滚动 {i + 1} 次后找到控件: {control}")
                return True

        # 向上滚动查找
        for i in range(max_scroll_up):
            pyautogui.scroll(scroll_amount)
            time.sleep(scroll_interval)
            if control.Exists(0):
                logger.info(f"向上滚动 {i + 1} 次后找到控件: {control}")
                return True

        logger.warning(f"滚动查找控件未找到: {control}")
        return False

    def find_element_by_scroll_up_and_down(self, template_path, max_scroll_down=20, max_scroll_up=20):
        """
        查找图标或者图像，如果找不到则执行滚轮滚动，直到找到或达到最大滚动次数。
        :param template_path: 模版路径地址
        :param max_scroll_count: 滚动次数
        :param max_scroll_up: 最大向上滚动次数
        :return: 找到的图标或者图片对象，如果未找到返回 None
        """
        try:
            element = ScreenElement(project_root.getImagePath(template_path))
            element.scroll_and_find(max_scroll_down, max_scroll_up)
            if element.exists():
                logger.info(f"在滚动查找时找到控件: {element.find()}")
            return element.exists()
        except Exception as e:
            logger.error(f"查找控件时发生异常: {e}")

    # ===========================================资源管理器操作方法=============================================================
    def input_file_path(self, file_path):
        """
        在文件管理器，输入需要导入音效的路径地址
        获取导入文件路径
        举例 ：file_path = GetPath().getProjectRoot() + r"\\resources\\testdata\\community\\video"

        """
        # 定位并点击“桌面”以展开路径（可选，用于确保路径栏可用）
        try:
            # 文件管理器页面，点击左侧导航栏，桌面
            desktop_item_control1 = self.main_window.PaneControl(Name='文件夹布局窗格', ClassName='Element', Depth=4).TreeItemControl(Name='桌面', Depth=3).TreeItemControl(Name='此电脑', Depth=1)
            if not auto.WaitForExist(desktop_item_control1, 1):
                logger.warning("[警告] 未找到桌面树项")
            BasePage.click(self, desktop_item_control1)
        except Exception as e:
            logger.info(f"[信息] 点击桌面树项时出错（可忽略）: {e}")

        # 点击地址栏并输入目标路径
        try:
            address_toolbar_control = self.main_window.PaneControl(ClassName='WorkerW', Depth=2).PaneControl(ClassName='Address Band Root', Depth=2).ToolBarControl(Name='地址: 此电脑', ClassName='ToolbarWindow32', Depth=3)
            if auto.WaitForExist(address_toolbar_control, 1):
                # 点击地址栏
                BasePage.click(self, address_toolbar_control)

                auto.SendKeys(file_path, waitTime=0.5)
                auto.SendKeys('{Enter}', waitTime=0.5)
                time.sleep(0.5)  # 等待文件列表加载
            else:
                logger.warning("[警告] 未找到地址栏，可能路径已正确。")
        except Exception as e:
            logger.error(f"[错误] 设置路径时出错: {e}")





    def open_file(self, file_name):
        """
        在文件管理器页，选择文件，点击打开选中的文件

        """
        # 文件空间元素地址
        self._select_file(file_name)
        file_name_control = self.main_window.ButtonControl(Name='打开(O)', ClassName='Button', Depth=2)
        control_raise(file_name_control, '文件管理器-打开按钮')
        BasePage.click(self, file_name_control)
    # ===========================================================资源管理器操作方法====================================================================================

    def wait_for_image_disappear(self, image_path, timeout=10, interval=0.5):
        """
        在规定时间内循环等待控件元素消失
        :param image_path: 图片路径
        :param timeout: 超时时间
        :param interval: 检查间隔
        :return: True 表示元素消失，False 表示超时
        """
        element = ScreenElement(project_root.getImagePath(image_path))
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not element.exists():
                return True
            time.sleep(interval)
        return False

    def wait_for_image_appear(self, image_path, timeout=30, interval=0.5):
        """
        在规定时间内循环等待控件元素显示   image_path
        :param image_path: 图片路径
        :param timeout: 超时时间
        :param interval: 检查间隔
        :return: True 表示元素显示，False 表示超时未显示
        """
        element = ScreenElement(project_root.getImagePath(image_path))
        return element.exists(timeout=timeout)

    def wait_for_control_disappear(self,control,timeout=30, interval=0.5):
        """
        循环等待控件消失  control
        :param active_window: 主窗口对象 (AutomationElement)
        :param timeout: 最大等待时间 (秒)
        :param interval: 每次检查的间隔 (秒)
        :return: 元素消失返回 True，超时返回 False
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 检查元素是否存在
                if not control.Exists(0):  # 0 表示立即检查，不等待
                    return True
            except Exception:
                # 如果查找过程中抛出异常，通常也意味着元素已消失
                return True

            # 休眠一小段时间，避免 CPU 占用过高
            time.sleep(interval)

        # 超时仍未消失
        return False
    def wait_for_control_appear(self,control,timeout=600, interval=0.5):
        """
        循环等待控件消失  control
        :param active_window: 主窗口对象 (AutomationElement)
        :param timeout: 最大等待时间 (秒)
        :param interval: 每次检查的间隔 (秒)
        :return: 元素消失返回 True，超时返回 False
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 检查元素是否存在
                if control.Exists(0):  # 0 表示立即检查，不等待
                    return True
            except Exception:
                # 如果查找过程中抛出异常，通常也意味着元素未出现
                return False

            # 休眠一小段时间，避免 CPU 占用过高
            time.sleep(interval)

        # 超时仍未出现
        return False



    def find_element_and_click(self, template_path, timeout=None):
        """
        找到图标或者图像元素并且点击操作
        :param template_path: 图片路径
        :param timeout: 超时时间（秒），默认为None即不等待只查找一次
        :return: None
        """
        element = ScreenElement(project_root.getImagePath(template_path))
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout

        if element.click(delay=1, timeout=timeout):
            return
        else:
            if timeout > 0:
                raise RuntimeError(f"在 {timeout} 秒内未找到目标元素图片: {template_path}")
            else:
                raise RuntimeError(f"未找到目标元素图片: {template_path}")

    def find_element(self, template_path, timeout=None):
        """
        查找图标或者图像
        :param template_path: 模版路径地址
        :param timeout: 超时时间（秒），默认为None则使用类里面默认的超时
        :return: 找到返回 True，未找到返回 False
        """
        element = ScreenElement(project_root.getImagePath(template_path))

        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout

        return element.exists(timeout=timeout)

    def find_element_and_input(self, template_path, content, timeout=None):
        """
        查找图像元素并输入内容
        :param template_path: 模版路径地址
        :param content: 要输入的内容
        :param timeout: 超时时间（秒），默认为None即不等待只查找一次
        :return: bool - 输入成功返回 True，失败返回 False
        """
        element = ScreenElement(project_root.getImagePath(template_path))
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout

        if element.exists(timeout=timeout):
            element.click()
            time.sleep(0.2)
            auto.SendKeys(content, waitTime=0.3)
            logger.info(f"已在图像元素位置输入内容: {content}")
            return True
        else:
            if timeout > 0:
                logger.error(f"在 {timeout} 秒内未找到图像元素：{template_path}")
            else:
                logger.error(f"未找到图像元素：{template_path}")
            return False

    def hover_to_element(self, template_path, timeout=None):
        """
        移动鼠标到图标或者图像元素位置
        :param template_path: 模版路径地址
        :param timeout: 超时时间（秒），默认为None即不等待只查找一次
        :return: None
        """
        # 实例化
        element = ScreenElement(project_root.getImagePath(template_path))
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout

        if element.exists(timeout=timeout):
            position = element.find()
            logger.info(
                f"{template_path}控件元素已经找到！！！================================================================位置坐标：{position}")
            # 实例化鼠标控制器
            mouse_controller = SlowMouseController()
            mouse_controller.move_to(position[0], position[1], duration=1.0)
            time.sleep(0.5)
        else:
            if timeout > 0:
                raise TargetElementNotFoundError(f"在 {timeout} 秒内未找到目标元素：{template_path}")
            else:
                raise TargetElementNotFoundError(f"未找到目标元素：{template_path}")

    def click_relative_to_element(self, template_path, offset_x=0, offset_y=0, timeout=None):
        """
        找到相对图标或者图像元素位置并点击
        :param template_path: 模版路径地址
        :param offset_x: x轴偏移量
        :param offset_y: y轴偏移量
        :param timeout: 超时时间（秒），默认为None即不等待只查找一次
        :return: None
        """

        # 实例化
        element = ScreenElement(project_root.getImagePath(template_path))
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout

        if element.exists(timeout=timeout):
            logger.info(
                f"{template_path} 控件元素存在！！！================================================================坐标位置：{element.find()}")
            return element.click_relative_to_element(offset_x=offset_x, offset_y=offset_y)
        else:
            if timeout > 0:
                raise TargetElementNotFoundError(f"在 {timeout} 秒内未找到目标元素：{template_path}")
            else:
                raise TargetElementNotFoundError(f"未找到目标元素：{template_path}")

    def find_control_and_click_relative_cursor(self, control, offset_x=0, offset_y=0, timeout=None, description=''):
        """
        先查找控件元素，若找到则获取当前鼠标位置，再相对鼠标位置偏移缓慢移动并点击
        :param control: uiautomation.Control 控件对象
        :param offset_x: 相对鼠标位置的x轴偏移量
        :param offset_y: 相对鼠标位置的y轴偏移量
        :param timeout: 等待控件出现的超时时间（秒）
        :param description: 控件描述，用于异常提示
        :return: bool - 是否点击成功
        """
        timeout = timeout if timeout is not None else self.default_timeout
        control_raise(control, description, timeout)
        cursor_x, cursor_y = self._get_cursor_position()
        cursor_x = self._to_int(cursor_x)
        cursor_y = self._to_int(cursor_y)
        logger.info(f"控件已找到，当前鼠标位置: ({cursor_x}, {cursor_y})")
        target_x = cursor_x + offset_x
        target_y = cursor_y + offset_y
        self._smooth_move_to(target_x, target_y)
        self._mouse_left_down()
        time.sleep(self.slow_press_duration)
        self._mouse_left_up()
        time.sleep(0.1)
        logger.info(f"已相对鼠标位置点击: 偏移({offset_x}, {offset_y}), 目标坐标({target_x}, {target_y})")
        return True

    def click_mouse_relative_positon(self, offset_x=0, offset_y=0):
        """
         mouse cursor positon  相对鼠标当前停止位置的偏移位置
        点击相对 template_path图标的偏移位置
        :param offset_x: x轴偏移量
        :param offset_y: y轴偏移量
        :return: None
        """
        # 获取鼠标当前位置坐标 (返回 tuple: x, y)
        center = auto.GetCursorPos()
        logger.info(f"鼠标位置: X={center[0]}, Y={center[1]}")
        # 计算目标坐标  local
        target_x = center[0] + offset_x
        target_y = center[1] + offset_y

        # 实例化
        mouse = SlowMouseController()
        mouse.click(target_x, target_y, duration=1.0, clicks=1)
        logger.info(f"已点击元素相对位置: ({offset_x}, {offset_y})")

    def send_to_contents(self,template_path, str_content, offset_x,offset_y, timeout=None):
        """
        发送内容
        :param template_path: 模版路径地址
        :param str_content: 发送内容
        :param offset_x: x轴偏移量
        :param offset_y: y轴偏移量
        :param timeout: 超时时间（秒），默认为None即不等待只查找一次
        :return: None
        """
        # 实例化
        element = ScreenElement(project_root.getImagePath(template_path))
        # 如果用户自定义了超时时间，则使用自定义的超时时间，没有定义则使用类里面默认的超时
        timeout = timeout if timeout is not None else self.default_timeout

        if element.exists(timeout=timeout):
            element.click_relative_to_element(offset_x=offset_x, offset_y=offset_y)
            time.sleep(1)
            BasePage.send_keys(str_content)
        else:
            if timeout > 0:
                raise TargetElementNotFoundError(f"在 {timeout} 秒内未找到目标元素：{template_path}")
            else:
                raise TargetElementNotFoundError(f"未找到目标元素：{template_path}")
    def send_contents(self,str_content):
        """
            输入字符
        """
        BasePage.send_keys(str_content)

    def enter(self):
        """
        输入回车键
        """
        BasePage.send_keys('{Enter}')
    def selectAll(self):
        """
        全选
        """
        BasePage.send_keys('{Ctrl}{A}')

    def delete(self):
        """
        删除
        """
        BasePage.send_keys('{Delete}')
    def copy(self):
        """
        复制
        """
        BasePage.send_keys('{Ctrl}{C}')

    def paste(self):
        """
        粘贴
        """
        BasePage.send_keys('{Ctrl}{V}')

    def clip_output(self):
        """
        把电脑剪贴板上复制的内容输出
        """
        text = pyperclip.paste()
        logger.info(f"===复制的文字为：{text}")
        return text


    #一般情况不使用，不推荐使用
    @staticmethod
    def move_to(x: int, y: int, wait_time: float = 0.5):
        """移动鼠标到指定坐标"""
        auto.MoveTo(x, y, waitTime=wait_time)

    @staticmethod
    def send_keys(keys: str, wait_time: float = 0.5):
        """
        发送键盘按键组合类型
        keys：'{Ctrl}{A}'  {Ctrl}{C}  {Ctrl}{V}  {Delete}  {Backspace}
        auto.SendKeys("Hello, this is a test message!")
        """
        auto.SendKeys(keys, waitTime=wait_time)

    @staticmethod
    def click_coord(x: int, y: int, wait_time: float = 0.5):
        """直接点击坐标"""
        auto.Click(x, y, waitTime=wait_time)

    @staticmethod
    def allure_screenshot(name="截图"):
        """
        截取当前主窗口并附加到Allure报告
        :param name: 截图步骤描述
        """
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        tmp.close()
        try:
            pyautogui.screenshot(tmp.name)
            allure.attach.file(tmp.name, name=name, attachment_type=allure.attachment_type.PNG)
            logger.info(f"已附加截图到Allure报告: {name}")
        except Exception as e:
            logger.error(f"截图附加到Allure报告失败: {e}")
        finally:
            os.unlink(tmp.name)



if __name__ == '__main__':
    main_window = uiautomation.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    # 激活窗口
    main_window.SetActive()
    # element = ScreenElement(project_root.getImagePath(r"\resources\images\nav4_file_voice_changer\66.png"))
    # position = element.find()
    # logger.info(f"position图片坐标位置================================================================：{position}")

    basepage = BasePage(main_window)
    # basepage.find_element_and_click(GetPath().getImagePath("nav3_community_library/upload_10.png"))
    # basepage.click_relative_to_element(GetPath().getImagePath("nav3_community_library/upload_10.png"), 0, 70)

    basepage.click_relative_to_element(GetPath().getImagePath("nav3_community_library/upload_9.png"), 0, 70)
