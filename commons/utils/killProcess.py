
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn


import ctypes
import sys
import psutil
from commons.utils.myLogging import get_logger

logger = get_logger()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        logger.info("需要管理员权限，正在请求...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def kill_process_by_name(name):
    killed = False
    for p in psutil.process_iter(['pid', 'name']):
        if p.info['name'] == name:
            try:
                p.kill()
                logger.info(f"已终止: {name} (PID: {p.info['pid']})")
                killed = True
            except psutil.AccessDenied:
                logger.error(f"无权限终止 PID {p.info['pid']} (可能需要更高权限)")
    return killed

# if __name__ == "__main__":
#     run_as_admin()  # 自动提权
#     if kill_process_by_name('easeus.voicewave.exe'):
#         print("操作完成")
#     else:
#         print("未找到目标进程")