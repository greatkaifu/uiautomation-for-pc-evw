#!/usr/bin/python3
# -*- coding : utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn
import time

import pytest
import subprocess
from commons.utils.configmanager import ConfigManager
from commons.utils.killProcess import kill_process_by_name
from commons.utils.languageSet import LanguageSet
from commons.utils.readconfig import INIConfigReader
from commons.utils.myLogging import get_logger
from pom.voicewave_closeprogram_page import CloseProgram
from pom.voicewave_discount_alert import DiscountAlert

try:
    import uiautomation as auto
except Exception:  # noqa: BLE001 - 兼容纯接口环境/无 UIAutomation 依赖
    auto = None

logger = get_logger()



# # 模版路径地址
# # 拼接完整图片路径（字符串）
# template_path = "nav1_real_time_voice_changer/real_time_voice_changer_scroll_1.png"
#
# position = ScreenElement(getImagePath(template_path))


# @pytest.fixture(scope="function")
# def start_program():
#     # 如果激活了，则清除激活码，让程序置置为未激活状态
#     manager=ConfigManager()
#     # 删除ini文件，制造未激活的新用户环境
#     manager.delete_voice_wave_ini()
#     #清除激活信息
#     manager.delete_active_file("7854852e2bb383d7ac.bin")
#     # 启动程序
#     print("\n--- 前置：启动应用程序，拉取最新的ini配置确保是未激活的新用户环境 ---")
#     #在启动之前确保启动的进程不存在
#     kill_process_by_name("easeus.voicewave.exe")
#     program_path = r'C:\Program Files (x86)\EaseUS\VoiceWave\bin\easeus.voicewave.exe'
#     subprocess.Popen(program_path)
#     time.sleep(12)
#     # 关闭程序
#     kill_process_by_name("easeus.voicewave.exe")
#     yield
#
# @pytest.fixture(scope="session")
# def install_program():
#     """
#     安装程序
#     :return:
#     """
#     # 确保安装时确保进程不存在
#     kill_process_by_name("easeus.voicewave.exe")
#     # 如果激活了，则清除激活码，让程序置置为未激活状态
#     print("\n--- 前置：开始设置测试环境 ---")
#     installer = SilentInstaller(
#         exe_path=r"C:\Users\admin\Desktop\EVW\3.3.2\2026-01-19_13.39(v3.3.2 ab测试)\free\voice_wave.exe",
#         lang='en',  # 可切换为 'en'
#         custom_args=[
#             '/DIR=C:\\Program Files (x86)\\EaseUS\\VoiceWave',
#             '/NOICONS'  # 不创建桌面快捷方式（Inno参数）
#         ],
#         timeout=300
#     )
#     success = installer.install()
#     if success:
#         print("[成功] 安装成功。")
#         # 注意是在English环境下调试的代码，注意程序安装语言环境是English
#         program_path = r'C:\Program Files (x86)\EaseUS\VoiceWave\bin\easeus.voicewave.exe'
#
#         # 启动程序
#         print("正在启动 EaseUS VoiceWave...")
#         # 必须程序重启后，才会拉取最新的 VoiceWave.ini配置文件
#         subprocess.Popen(program_path)
#         time.sleep(12)
#         # 等待主窗口出现（最多 30 秒）
#         print("等待主窗口加载...")
#         main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
#         if not main_win.Exists(maxSearchSeconds=30):
#             print("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
#             exit(1)
#
#         print("[成功] 程序已启动并获取到主窗口。")
#         # 确保程序已经启动完成，已经把响应的配置文件拉取到
#         kill_process_by_name("easeus.voicewave.exe")
#     else:
#         print("[错误] 安装失败。")
#         exit(1)

#
#
# # 控制全局
# @pytest.fixture(autouse=True,scope="session")
# def wb():
#     # 创建设置浏览器对象
#     options = Options()
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     # 关键：执行完不自动关闭浏览器
#     options.add_experimental_option("detach", True)
#     # 排除 enable-automation 开关，去除自动化控制提示
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     # options.add_experimental_option('useAutomationExtension', False)
#     # 禁用自动化特征检测
#     options.add_argument('--disable-blink-features=AutomationControlled')
#
#     # # 获取当前脚本所在目录的父级（可根据项目结构调整）
#     # PROJECT_ROOT = Path(__file__).parent.parent.resolve()
#     # driver = webdriver.Chrome(service=Service(str(PROJECT_ROOT /"python-uiautomation-for-pc-evw" /"chromedriver.exe")), options=options)
#     path=getProjectRoot()+"\chromedriver.exe"
#     driver = webdriver.Chrome(service=Service(path), options=options)
#
#     # 窗口最大化
#     driver.maximize_window()
#     #返回 driver
#     yield driver
#     time.sleep(6)
#
#     # 清理：关闭浏览器
#     driver.quit()


@pytest.fixture(scope="module") # session、 module 、class 级别，每个测试模块文件执行一次
def active_window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 程序启动完成后，确保程序已经启动完成，已经把响应的配置文件拉取到
    # 在ini配置文件添加 SHOW_EXIT_WINDOW=false 在关闭额程序中，则不会弹出二次确认弹窗。
    manager.set_show_exit_window_false()
    manager.set_close_is_exit()

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)


    # 等待主窗口出现（最多 60 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        pytest.exit("未能找到主窗口，脚本退出。")

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    yield main_win # yield返回数据给测试用例


    #
    # print("\n--- 后置：关闭程序清理测试环境 ---")
    # # 模拟关闭应用程序
    # program = CloseProgram(main_win)
    # # 关闭程序
    # program.close_program()
    # # 确保下次应用重启可以正常启动
    # kill_process_by_name("easeus.voicewave.exe")

@pytest.fixture(params=["English"],scope="function") #function 级别，每个测试用例执行一次
def newuser_language_window(request):
    """
    未激活的新用户环境
    """
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 程序启动完成后，确保程序已经启动完成，已经把响应的配置文件拉取到
    # 在ini配置文件添加 SHOW_EXIT_WINDOW=false 在关闭额程序中，则不会弹出二次确认弹窗。
    manager.set_show_exit_window_false()
    manager.set_close_is_exit()
    # 制造未激活新用户环境，并且保证ini配置里面时间是当前运行时间
    manager.delete_voice_wave_ini()


    #通过修改注册表，切换语言
    page = LanguageSet()
    page.open_and_control_regedit(request.param)

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)


    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    # yield返回数据给测试用例
    yield main_win, request.param

    # print("\n--- 后置：关闭程序清理测试环境 ---")
    # # 模拟关闭应用程序
    # program = CloseProgram(main_win)
    # # 关闭程序
    # program.close_program()
    # # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")






@pytest.fixture(params=["English"],scope="function") #function 级别，每个测试用例执行一次
def olduser_language_window(request):
    """
    未激活的老用户环境
    """
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 制造未激活老用户环境，启动弹窗展示问题
    # 修改INI文件中NEW_USER_LAUNCH_TIME字段的日期值（提前 / 延后指定天数）
    manager.modify_time()
    # 产品设计是每天启动弹窗只弹一次
    # 删除INI文件中以
    # START_UP_DISCOUNT_WIDGET_SHOW_TIME =
    # 保证每次启动都会有弹窗显示
    manager.delete_start_time()

    #通过修改注册表，切换语言
    page = LanguageSet()
    page.open_and_control_regedit(request.param)

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)


    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    # yield返回数据给测试用例
    yield main_win, request.param

    # print("\n--- 后置：关闭程序清理测试环境 ---")
    # # 模拟关闭应用程序
    # program = CloseProgram(main_win)
    # # 关闭程序
    # program.close_program()
    # # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")

# @pytest.fixture(params=["English","French","German","Italian","Korean","Portuguese","Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"],scope="function") #function 级别，每个测试用例执行一次
#

@pytest.fixture(params=["Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"],scope="function") #function 级别，每个测试用例执行一次
def creation_language_window(request):
    """
    未激活的新用户环境
    """
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 程序启动完成后，确保程序已经启动完成，已经把响应的配置文件拉取到
    # 在ini配置文件添加 SHOW_EXIT_WINDOW=false 在关闭额程序中，则不会弹出二次确认弹窗。
    manager.set_show_exit_window_false()
    manager.set_close_is_exit()
    # # 制造未激活新用户环境，并且保证ini配置里面时间是当前运行时间
    # manager.delete_voice_wave_ini()


    #通过修改注册表，切换语言
    page = LanguageSet()
    page.open_and_control_regedit(request.param)

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)


    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    # yield返回数据给测试用例
    yield main_win, request.param



    # print("\n--- 后置：关闭程序清理测试环境 ---")

    # # 模拟关闭应用程序
    # program = CloseProgram(main_win)
    # # 关闭程序
    # program.close_program()
    # # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")

@pytest.fixture(scope="function") #function 级别，每个测试用例执行一次
def login_window():
    """
    未激活的新用户环境
    """
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 程序启动完成后，确保程序已经启动完成，已经把响应的配置文件拉取到
    # 在ini配置文件添加 SHOW_EXIT_WINDOW=false 在关闭额程序中，则不会弹出二次确认弹窗。
    manager.set_show_exit_window_false()
    manager.set_close_is_exit()
    # # 制造未激活新用户环境，并且保证ini配置里面时间是当前运行时间
    manager.delete_voice_wave_ini()

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)


    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    # yield返回数据给测试用例
    yield main_win



    # print("\n--- 后置：关闭程序清理测试环境 ---")

    # # 模拟关闭应用程序
    # program = CloseProgram(main_win)
    # # 关闭程序
    # program.close_program()
    # # 确保下次应用重启可以正常启动
    # kill_process_by_name("easeus.voicewave.exe")


@pytest.fixture(scope="function") # session、 module 、class 级别，每个测试模块文件执行一次
def active_window_function():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 程序启动完成后，确保程序已经启动完成，已经把响应的配置文件拉取到
    # 在ini配置文件添加 SHOW_EXIT_WINDOW=false 在关闭额程序中，则不会弹出二次确认弹窗。
    manager.set_show_exit_window_false()
    manager.set_close_is_exit()

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")
    logger.info(f"================{program_path}")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)


    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    yield main_win # yield返回数据给测试用例



    logger.info("\n--- 后置：关闭程序清理测试环境 ---")
    # 模拟关闭应用程序
    program = CloseProgram(main_win)
    # 关闭程序
    program.close_program()
    # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")


@pytest.fixture(scope="module") # session、 module 、class 级别，每个测试模块文件执行一次
def window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 删除ini配置文件，确保用户在关闭程序时，退出方式为初始状态的退出逻辑
    manager.delete_voice_wave_ini()

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")
    logger.info(f"================{program_path}")


    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)
    # 程序启动完成后，确保程序已经启动完成，已经把响应的配置文件拉取到
    # 在ini配置文件添加 SHOW_EXIT_WINDOW=false 在关闭额程序中，则不会弹出二次确认弹窗。
    manager.set_show_exit_window_false()

    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    yield main_win # yield返回数据给测试用例



    logger.info("\n--- 后置：关闭程序清理测试环境 ---")
    # 模拟关闭应用程序
    program = CloseProgram( main_win)
    # 关闭程序
    program.close_program()
    # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")


@pytest.fixture(scope="function") # session、 module 、class 级别，每个测试模块文件执行一次
def bottom_window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 删除ini配置文件，确保用户在关闭程序时，退出方式为初始状态的退出逻辑
    manager.delete_voice_wave_ini()
    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read=INIConfigReader()
    program_path =read.getconfig("install","path")
    logger.info(f"================{program_path}")
    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)

    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")

    # 模拟启动应用程序
    yield main_win # yield返回数据给测试用例

    logger.info("\n--- 后置：关闭程序清理测试环境 ---")
    # 模拟关闭应用程序
    program = CloseProgram( main_win)
    # 关闭程序
    program.close_program()
    # 弹出二次确认弹窗，选择退出程序方式
    program.select_exit_way()
    # 点击二次确认退出OK
    program.click_program_ok()

    # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")



@pytest.fixture(scope="class") # session、 module 、class 级别，每个测试模块文件执行一次
def main_window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    manager=ConfigManager()
    # 删除ini配置文件，就是未激活的新用户
    manager.delete_voice_wave_ini()
    manager.delete_active_file("7854852e2bb383d7ac.bin")

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read = INIConfigReader()
    program_path = read.getconfig("install", "path")
    logger.info(f"================{program_path}")
    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)

    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")
    # 窗口设置激活
    # main_window.SetActive()
    # 窗口置顶处理
    # main_window.SetTopmost(True)

    # 模拟启动应用程序
    yield main_win # yield返回数据给测试用例

    logger.info("\n--- 后置：关闭程序清理测试环境 ---")
    page=DiscountAlert(main_win)
    # 关闭启动未激活新用户启动弹窗
    page.close_newuser_start_alert()
    # 模拟关闭应用程序
    program = CloseProgram( auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1))
    program.close_program()
    # 关闭未激活新用户挽留弹窗
    page.close_newuser_Wait_alert_second()
    # 选择退出程序方式
    CloseProgram(main_win).select_exit_way()
    # 点击二次确认退出OK
    CloseProgram(main_win).click_program_ok()
    # 确保下次应用重启可以正常启动
    kill_process_by_name("easeus.voicewave.exe")


@pytest.fixture(scope="function") # session、 module 、class 级别，每个测试模块文件执行一次
def old_main_window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    #在启动之前确保启动的进程不存在
    kill_process_by_name("easeus.voicewave.exe")
    logger.info("修改时间")
    # 首先保证该用户是一个未激活用户
    # 实例化一个配置管理器
    manager=ConfigManager()

    # 确保是一个未激活的老用户
    manager.delete_start_time()
    # 修改 时间，确保是未激活的老用户
    manager.modify_time()
    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read = INIConfigReader()
    program_path = read.getconfig("install", "path")
    logger.info(f"================{program_path}")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)

    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    old_main_window = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not old_main_window.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")
    # 窗口设置激活
    # main_window.SetActive()
    # 窗口置顶处理
    # main_window.SetTopmost(True)

    # 模拟启动应用程序
    yield old_main_window # yield返回数据给测试用例


    # print("\n--- 后置：关闭程序清理测试环境 ---")
    #选择退出程序方式
    CloseProgram(old_main_window).select_exit_way()
    # 点击二次确认退出OK
    CloseProgram(old_main_window).click_program_ok()
    time.sleep(2)
    kill_process_by_name("easeus.voicewave.exe")




@pytest.fixture(scope="class") # session、 module 、class 级别，每个测试模块文件执行一次
def new_main_window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    logger.info("修改时间")
    manager=ConfigManager()
    # 删除ini文件，制造未激活的新用户环境
    manager.delete_voice_wave_ini()

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read = INIConfigReader()
    program_path = read.getconfig("install", "path")
    logger.info(f"================{program_path}")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)

    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    main_win = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not main_win.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")
    # 窗口设置激活
    # main_window.SetActive()
    # 窗口置顶处理
    # main_window.SetTopmost(True)

    # 模拟启动应用程序
    yield main_win # yield返回数据给测试用例

    # print("\n--- 后置：关闭程序清理测试环境 ---")
    # 选择退出程序方式
    CloseProgram(old_main_window).select_exit_way()
    # 点击二次确认退出OK
    CloseProgram(old_main_window).click_program_ok()
    time.sleep(2)
    kill_process_by_name("easeus.voicewave.exe")


@pytest.fixture(scope="function") # session、 module 、class 级别，每个测试模块文件执行一次
def Inactive_main_window():
    if auto is None:
        pytest.skip("当前环境未安装 uiautomation，跳过 UI 用例相关 fixture")
    logger.info("\n--- 前置：开始设置测试环境 ---")
    #在启动之前确保启动的进程不存在
    kill_process_by_name("easeus.voicewave.exe")
    # 如果激活了，则清除激活码，让程序置置为未激活状态
    manager=ConfigManager()
    # 如果激活了，则清除激活码，让程序置置为未激活状态
    manager.delete_active_file("7854852e2bb383d7ac.bin")
    # 制造未激活新用户环境，并且保证ini配置里面时间是当前运行时间
    manager.delete_voice_wave_ini()

    # 注意是在English环境下调试的代码，注意程序安装语言环境是English
    read = INIConfigReader()
    program_path = read.getconfig("install", "path")
    logger.info(f"================{program_path}")

    # 启动程序
    logger.info("正在启动 EaseUS VoiceWave...")
    subprocess.Popen(program_path)

    # 等待主窗口出现（最多 30 秒）
    logger.info("等待主窗口加载...")
    old_main_window = auto.WindowControl(Name='EaseUS VoiceWave', ClassName='MainWidget', Depth=1)
    if not old_main_window.Exists(maxSearchSeconds=120):
        logger.error("[错误] 未能在 20 秒内找到主窗口，脚本退出。")
        exit(1)

    logger.info("[成功] 程序已启动并获取到主窗口。")
    # 窗口设置激活
    # main_window.SetActive()
    # 窗口置顶处理
    # main_window.SetTopmost(True)

    # 模拟启动应用程序
    yield old_main_window # yield返回数据给测试用例


    # print("\n--- 后置：关闭程序清理测试环境 ---")
    #选择退出程序方式
    CloseProgram(old_main_window).select_exit_way()
    # 点击二次确认退出OK
    CloseProgram(old_main_window).click_program_ok()
    time.sleep(1)


@pytest.fixture(scope="session")
def sensors_capture():
    """
    神策埋点抓包 fixture（方案B）。
    session 级：整个测试会话期间保持 mitmproxy 代理与系统代理开启。
    使用时在测试用例参数中将其置于窗口 fixture 之前，确保代理先于应用启动生效。

    用法：
        def test_xxx(sensors_capture, main_window):
            sensors_capture.clear()
            # ... UI 操作触发埋点 ...
            sensors_capture.assert_event_reported("event_name")
    """
    try:
        from commons.utils.sensorsCapture import SensorsCapture
        cap = SensorsCapture()
        cap.start()
    except Exception as e:
        pytest.skip(f"埋点抓包不可用（需 pip install mitmproxy）: {e}")
        return
    yield cap
    try:
        cap.stop()
    except Exception as e:
        logger.warning(f"停止埋点抓包异常: {e}")

