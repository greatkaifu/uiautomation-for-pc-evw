#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : voicewave_file_voicechanger_page.py




import time

from bases.captureScreen import ScreenElement
from commons.utils.getProjectRroot import GetPath
from commons.utils.myLogging import get_logger
import uiautomation as auto
from bases.basePage import BasePage

logger = get_logger()
# 实例化，获取项目根目录
project_root=GetPath()

class  FileVoiceChangerPage(BasePage):
    """EaseUS VoiceWave 主界面操作封装"""

    def __int__(self, main_window):
        super().__init__(main_window)

    def import_btn_filemanager(self,file_path):
        """
        在FileVoiceChanger页，点击 import按钮，进入文件管理器页

        """

        # 进入 Voice Changer 功能（左侧导航第4项，foundIndex=4）
        nav_list = self.main_window.ListControl(ClassName='CNaviListWidget', Depth=5)
        voice_changer_item = nav_list.ListItemControl(foundIndex=4, Depth=1)
        if voice_changer_item.Exists(maxSearchSeconds=5):
            voice_changer_item.Click()
            logger.info("已点击进入 Voice Changer 功能。")
        else:
            logger.warning("未找到 Voice Changer 导航项，继续执行...")


        # 等待并点击 Import按钮 控件（首次进入）
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4) \
            .GroupControl(ClassName='QWidget', Depth=3) \
            .ButtonControl(Name='Import', ClassName='CustomBtn', Depth=3)
        # # 等待并点击 Import按钮 控件（首次进入）
        # control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).CustomControl(ClassName='AnimationStackedWidget', Depth=1).ButtonControl(Name='导入', ClassName='CustomBtn', Depth=5)



        # 等待按钮出现
        if auto.WaitForExist(control, 1):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击upload_button 按钮功能。")

        else:
            logger.info(f"控制元素未出现")


        # 定位并点击“桌面”以展开路径（可选，用于确保路径栏可用）
        try:
            # 文件管理器页面，点击左侧导航栏，桌面
            desktop_item_control1 = self.main_window.PaneControl(Name='文件夹布局窗格', ClassName='Element', Depth=4).TreeItemControl(Name='桌面', Depth=3).TreeItemControl(Name='此电脑', Depth=1)
            BasePage.click(self, desktop_item_control1)
        except Exception as e:
            logger.info(f"点击桌面树项时出错（可忽略）: {e}")

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
                logger.warning("未找到地址栏，可能路径已正确。")
        except Exception as e:
            logger.error(f"设置路径时出错: {e}")


    def find_export(self):
        """
        在文件导入成功后页面，查找 export 按钮

        """
        # export 控件元素地址
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='AudioChangerSetting', Depth=3).ButtonControl(Name='Export', ClassName='CustomBtn', Depth=1)
        # 判断 export 控件是否存在
        if BasePage.find_control(self, control,timeout=10):
            return True
        #未找到返回 False
        return False

    def close_export_succeeded_alert(self):
        """
        在文件导入成功后页面，点击 export 按钮,导出成功后弹出提示弹窗。
        功能：关闭导出成功提示弹窗

        """
        close_btn =  self.main_window.GroupControl(ClassName='ExportWidget', Depth=1).ButtonControl(ClassName='QPushButton',Depth=1)
        if BasePage.find_control(self, close_btn,timeout=1):
            BasePage.click(self, close_btn)
            logger.info(f"已点击关闭按钮")
            return True
        logger.info(f"未找到关闭按钮")

    def export_succeeded_appear(self):
        """
        功能：判断是否出现导出成功提示弹窗
        :return:
        """
        # 导入完成弹窗上的关闭按钮元素
        export_succeeded = self.main_window.GroupControl(ClassName='ExportWidget', Depth=1).TextControl(
            Name='Export succeeded!', ClassName='QLabel', Depth=3)
        if BasePage.find_control(self, export_succeeded,timeout=1):
            return True
        logger.info(f"未找到导出成功提示弹窗")
        return False

    def check_output_path(self,file_path):
        """
        在文件管理器页，选择不同的格式文件

        """
        # 打开文件管理器按钮控件元素地址
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(ClassName='AudioChangerSetting', Depth=3).GroupControl(ClassName='QWidget', AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.AnimationStackedWidget.AudioVoiceChangerWidget.widget_rigetSetting.widget_saveSomeShowRect', Depth=1).GroupControl(ClassName='SavePathWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=2)
        # 等待按钮控件显示
        if auto.WaitForExist(control, 1):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击upload_button 按钮功能。")
        else:
            logger.info(f"控制元素未出现")

        # 定位并点击“桌面”以展开路径（可选，用于确保路径栏可用）
        try:
            # 文件管理器页面，点击左侧导航栏，桌面
            desktop_item_control1 = self.main_window.PaneControl(Name='文件夹布局窗格', ClassName='Element', Depth=4).TreeItemControl(Name='桌面 (已固定)', Depth=4)
            if not auto.WaitForExist(desktop_item_control1, 1):
                logger.info("[警告] 未找到桌面树项")
                #如果不存在，使用第二个
                desktop_item_control2 = self.main_window.PaneControl(Name='文件夹布局窗格', ClassName='Element', Depth=4).TreeItemControl(Name='桌面', Depth=3).TreeItemControl(Name='桌面 (已固定)', Depth=1)
                BasePage.click(self, desktop_item_control2)
            BasePage.click(self, desktop_item_control1)

        except Exception as e:
            logger.info(f"点击桌面树项时出错（可忽略）: {e}")

        # 点击地址栏并输入目标路径
        try:
            address_toolbar_control = self.main_window.PaneControl(ClassName='WorkerW', Depth=2).PaneControl(ClassName='Address Band Root', Depth=2).ToolBarControl(Name='地址: 桌面', ClassName='ToolbarWindow32', Depth=3)
            if auto.WaitForExist(address_toolbar_control, 1):
                # 点击地址栏
                BasePage.click(self, address_toolbar_control)

                auto.SendKeys(file_path, waitTime=0.5)
                auto.SendKeys('{Enter}', waitTime=0.5)
                time.sleep(0.5)  # 等待文件列表加载
            else:
                logger.warning("未找到地址栏，可能路径已正确。")
        except Exception as e:
            logger.error(f"设置路径时出错: {e}")
        control_select = self.main_window.ButtonControl(Name='选择文件夹', ClassName='Button', Depth=2)
        if BasePage.find_control(self, control_select,timeout=10):
            BasePage.click(self, control_select)
        else:
            logger.info("未找到选择文件夹按钮")

    def export_click(self):
        """
        在nav4 导入文件成功后的页面，操作点击 export按钮

        """
        #导出按钮控件元素路径
        control_export_btn = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
            ClassName='AudioChangerSetting', Depth=3).ButtonControl(Name='Export', ClassName='CustomBtn', Depth=1)
        BasePage.click(self, control_export_btn)

        # 配置等待参数
        timeout_seconds = 600  # 10 分钟 = 600 秒
        check_interval = 2  # 每 2 秒检查一次，避免 CPU 占用过高
        start_time = time.time()
        logger.info(f"开始等待 Export 按钮，最长等待 {timeout_seconds} 秒...")

        while True:
            try:
                # 尝试查找控件 (如果找不到，这里通常会抛出 LookupError 或 AttributeError)
                control_success_text = self.main_window.GroupControl(ClassName='ExportWidget', Depth=1).TextControl(Name='Export succeeded!', ClassName='QLabel', Depth=3)
                if BasePage.find_control(self, control_success_text,timeout=10):
                    # 如果代码运行到这里没有报错，说明控件找到了
                    logger.info(f"Export succeeded!已经找到。")
                    break  # 找到后立刻跳出循环，进入下一步

            except Exception as e:
                logger.info(f"[错误] 找不到 Export 按钮: {e}")
                # 计算已经等待了多久
                elapsed_time = time.time() - start_time

                if elapsed_time > timeout_seconds:
                    # 超过 10 分钟，抛出异常，让测试失败
                    error_msg = f"等待Export succeeded! 文案已经超时 ({timeout_seconds}秒)，控件仍未出现。"
                    logger.error(error_msg)
                    raise TimeoutError(error_msg)

                # 没超时，打印一下日志（可选），然后睡一会再试
                logger.info(f"未找到按钮，已等待 {elapsed_time:.1f} 秒，继续等待...")
                time.sleep(check_interval)


    def close_filemanager(self):
        """
        在文件管理器页，点击关闭按钮
        """
        # 关闭按钮控件路径
        close_btn_control=self.main_window.TitleBarControl(Depth=2).ButtonControl(Name='关闭', Depth=1)
        if auto.WaitForExist(close_btn_control, 1):
            # 继承
            BasePage.click(self, close_btn_control)
            logger.info(f"已点击nav4_page的文件管理器close_btn_control按钮")
        else:
            logger.warning("未找到关闭按钮，可能已关闭。")


    def filemanager_alert(self):
        """
        在FileVoiceChanger页，点击 import按钮，进入文件管理器页

        """

        # 进入 Voice Changer 功能（左侧导航第4项，foundIndex=4）
        nav_list = self.main_window.ListControl(ClassName='CNaviListWidget', Depth=5)
        voice_changer_item = nav_list.ListItemControl(foundIndex=4, Depth=1)
        if voice_changer_item.Exists(maxSearchSeconds=5):
            voice_changer_item.Click()
            logger.info("已点击进入 Voice Changer 功能。")
        else:
            logger.warning("未找到 Voice Changer 导航项，继续执行...")


        # 等待并点击 Import按钮 控件（首次进入）
        control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4) \
            .GroupControl(ClassName='QWidget', Depth=3) \
            .ButtonControl(Name='Import', ClassName='CustomBtn', Depth=3)

        # 等待按钮出现
        if auto.WaitForExist(control, 1):
            # 继承
            BasePage.click(self, control)
            logger.info(f"已点击upload_button 按钮功能。")
        else:
            logger.info(f"控制元素未出现")





    def select_file(self, file_name):
        """
        在文件管理器页，选择不同的格式文件

        """
        # if file_name == "sample.aac" or file_name == "sample.ac3" or file_name == "sample.mp2":
        #     control = self.main_window.ComboBoxControl(Name='文件类型(T):', ClassName='ComboBox', Depth=2)
        #     BasePage.click(self, control, timeout=2)
        #     element = ScreenElement(GetPath().getImagePath("nav4_file_voice_changer/file1.png"))
        #     element.click(delay=1)


        # 文件空间元素地址
        file_name_control = self.main_window.PaneControl(Name='文件夹布局窗格', ClassName='Element', Depth=4).PaneControl(Name='Shell 文件夹视图', ClassName='DUIListView', Depth=1).ListItemControl(Name=file_name, ClassName='UIItem', Depth=2).EditControl(Name='名称', ClassName='UIProperty', Depth=1)
        if auto.WaitForExist(file_name_control, 5):
            BasePage.click(self, file_name_control)
        else:
            logger.warning("未找到文件，请检查文件名。")

    def open_file(self, file_name):
        """
        在文件管理器页，选择文件，点击打开选中的文件

        """
        # 文件空间元素地址
        self.select_file(file_name)
        file_name_control = self.main_window.ButtonControl(Name='打开(O)', ClassName='Button', Depth=2)
        if auto.WaitForExist(file_name_control, 1):
            BasePage.click(self, file_name_control)
        else:
            logger.warning("未找到文件，请检查文件名。")


    def wait_element_disappear(self,control,timeout=30, interval=0.5):
        """
        循环等待上传过程弹窗取消按钮控件消失
        :param active_window: 主窗口对象 (AutomationElement)
        :param timeout: 最大等待时间 (秒)
        :param interval: 每次检查的间隔 (秒)
        :return: 元素消失返回 True，超时返回 False
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # # 【关键】在循环内部重新查找元素，确保获取最新的 UI 状态
                # cancle_btn = self.main_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(Name='Cancel', ClassName='CustomBtn', Depth=1)

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



    def back_btn_click(self):
        """
         在FileVoiceChanger页，点击 back按钮
        """
        # 返回按钮控件地址
        back_btn_control=self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).ButtonControl(Name='Back', ClassName='CustomBtn', Depth=3)
        # 等待按钮出现
        if auto.WaitForExist(back_btn_control, 1):
            # 继承
            BasePage.click(self, back_btn_control)
            logger.info(f"已点击nav4_page的back_btn_control按钮。")
        else:
            logger.info(f"控制元素未出现")


    def close_import_failed_alert(self):
        """
         导入视频无音频流文件，提示导入失败提示弹窗
         导入失败，点击弹窗上的关闭按钮
        """
        control=self.main_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(ClassName='QPushButton', Depth=1)

        if  not BasePage.find_control(self, control) :
            logger.info(f"未找到导入失败提示弹窗")
        BasePage.click(self, control)

    def import_failed_alert_click_ok(self):
        """
         导入视频无音频流文件，提示导入失败提示弹窗
         点击OK按钮弹窗关闭
        """
        control=self.main_window.GroupControl(ClassName='ImportProcessWidget', Depth=1).ButtonControl(Name='OK', ClassName='CustomBtn', Depth=1)

        if  not BasePage.find_control(self, control) :
            logger.info(f"未找到导入成功提示弹窗")
        BasePage.click(self, control)

    def file_convert_to_format(self,format_name):
        """
         导入音视频文件，转换成各种音视频文件
         导入转换成对应格式文件后，转换成成功,并且删除该文件，则返回 True 否则返回 false
        """

        # 转换格式按钮
        template_path = "nav4_file_voice_changer/select.png"
        # 当格式为 mov时
        if format_name == "MOV":
            try:
                control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
                    ClassName='AudioChangerSetting', Depth=3).GroupControl(ClassName='QWidget',
                                                                           AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.AnimationStackedWidget.AudioVoiceChangerWidget.widget_rigetSetting.widget_saveSomeShowRect',
                                                                           Depth=1).ListItemControl(Name=format_name,
                                                                                                    Depth=3)

                # 拼接完整图片路径（字符串）
                element = ScreenElement(project_root.getImagePath(template_path))
                # 找到该图标
                if not element.exists():
                    logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")
                # 计算找到图标的坐标，相对位置点击
                element.click_relative_to_element(offset_x=136, offset_y=72)
                element_soll=ScreenElement(project_root.getImagePath("nav4_file_voice_changer/soll.png"))
                postion=element_soll.find()
                # 移动到该图标坐标
                element_soll.move_to(postion[0], postion[1])
                auto.WheelDown(wheelTimes=1)
                # 鼠标移动
                BasePage.click(self, control)
            except Exception as e:
                logger.error(f"{e}")
                logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")
        elif format_name == "MP3":
            try:
                control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
                    ClassName='AudioChangerSetting', Depth=3).GroupControl(ClassName='QWidget',
                                                                           AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.AnimationStackedWidget.AudioVoiceChangerWidget.widget_rigetSetting.widget_saveSomeShowRect',
                                                                           Depth=1).ListItemControl(Name=format_name,
                                                                                                    Depth=3)

                # 拼接完整图片路径（字符串）
                element = ScreenElement(project_root.getImagePath(template_path))
                # 找到该图标
                if not element.exists():
                    logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")
                # 计算找到图标的坐标，相对位置点击
                element.click_relative_to_element(offset_x=136, offset_y=72)
                element_soll=ScreenElement(project_root.getImagePath("nav4_file_voice_changer/soll.png"))
                postion=element_soll.find()
                # 移动到该图标坐标
                element_soll.move_to(postion[0], postion[1])
                #向上滚动一次
                auto.WheelUp(wheelTimes=1)
                # 鼠标移动
                BasePage.click(self, control)
            except Exception as e:
                logger.error(f"{e}")
                logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")

        else:
            try:
                control = self.main_window.CustomControl(ClassName='QStackedWidget', Depth=4).GroupControl(
                    ClassName='AudioChangerSetting', Depth=3).GroupControl(ClassName='QWidget',
                                                                           AutomationId='FramelessWidget.widget_showRect.MainWidget.widget_context.stackedWidget_modules.AnimationStackedWidget.AudioVoiceChangerWidget.widget_rigetSetting.widget_saveSomeShowRect',
                                                                           Depth=1).ListItemControl(Name=format_name,
                                                                                                    Depth=3)

                # 拼接完整图片路径（字符串）
                element = ScreenElement(project_root.getImagePath(template_path))
                # 找到该图标
                if not element.exists():
                    logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")
                # 计算找到图标的坐标，相对位置点击
                element.click_relative_to_element(offset_x=136, offset_y=72)
                BasePage.click(self, control)
            except Exception as e:
                logger.error(f"{e}")
                logger.info(f"未找到 {project_root.getImagePath(template_path)} 图标")
































