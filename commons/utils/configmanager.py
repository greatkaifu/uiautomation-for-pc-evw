#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: leikaifu
# IDE    ：PyCharm
# @File : configmanager.py


import os
import re
import shutil
import sys
import ctypes
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple
import os
import re
from datetime import datetime, timedelta
from commons.utils.myLogging import get_logger

logger = get_logger()


class ConfigManager:
    """
    EaseUS VoiceWave 配置文件管理器
    提供配置文件的检测、删除、目录打开等操作，支持跨Windows系统兼容
    """

    def __init__(self):
        """
        初始化配置管理器
        """
        self.process_name="easeus.voicewave.exe"

    def _is_admin(self):
        """检查当前进程是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _run_as_admin(self):
        """以管理员身份重新启动当前脚本"""
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1
            )
            sys.exit(0)  # 当前进程退出，等待提权后的新进程执行
        except Exception as e:
            logger.error(f"提权失败: {e}")
            sys.exit(1)

    def _terminate_process_if_exists(self,process_name):
        """终止指定名称的进程（例如 easeus.voicewave.exe）"""
        try:
            result = subprocess.run(
                ['taskkill', '/f', '/im', process_name],
                capture_output=True,
                text=True,
                encoding='gbk'  # 中文系统兼容编码
            )
            if result.returncode == 0:
                logger.info(f"已成功终止进程: {process_name}")
            elif "找不到" in result.stderr or "无法终止" in result.stderr:
                logger.info(f"未检测到进程: {process_name}（可继续操作）")
            else:
                logger.error(f"终止进程时出现异常: {result.stderr.strip()}")
        except Exception as e:
            logger.error(f"终止进程时发生错误: {e}")

    def _delete_file_safely(self, filename):
        """
        安全删除目标目录下的指定文件

        参数:
            target_dir: 目标目录路径 (str)
            filename: 要删除的文件名 (str)
        """

        # ========== 可选：终止相关进程（避免文件被占用）==========
        self._terminate_process_if_exists(self.process_name)
        # 1. 校验文件名安全性（防止路径遍历攻击）
        if '..' in filename or ':' in filename or filename.startswith('\\'):
            logger.warning(f"非法文件名，可能包含路径遍历字符: {filename}")
            return False
        TARGET_DIR = r"C:\Program Files (x86)\EaseUS\VoiceWave\bin"  # 目标目录
        # 2. 构建完整路径并标准化
        file_path = Path(TARGET_DIR) / filename
        file_path = file_path.resolve()  # 转为绝对路径

        # 3. 二次校验：确保目标文件确实在目标目录内（防止符号链接绕过）
        target_dir_abs = Path(TARGET_DIR).resolve()
        if not str(file_path).startswith(str(target_dir_abs)):
            logger.error(f"安全校验失败：目标文件不在允许的目录范围内")
            return False

        # 4. 检查文件是否存在
        if not file_path.exists():
            logger.info(f"文件不存在: {file_path}")
            return False

        # 5. 尝试删除文件
        try:
            file_path.unlink()
            logger.info(f"文件删除成功: {file_path}")
            return True
        except PermissionError:
            logger.error(f"权限不足，无法删除文件: {file_path}")
            logger.info("请确保已关闭相关程序（如 VoiceWave），并以管理员身份运行脚本。")
            return False
        except Exception as e:
            logger.error(f"删除文件时发生错误: {e}")
            return False

    def delete_active_file(self, filename):
        """
        删除激活文件，制造未激活环境
        """
        # ========== 配置区域 ==========
        TARGET_DIR = r"C:\Program Files (x86)\EaseUS\VoiceWave\bin"  # 目标目录
        FILE_TO_DELETE = filename  # 请替换为实际要删除的文件名，或通过参数传入

        # 支持通过命令行参数传入文件名：python script.py target.dll
        if len(sys.argv) > 1:
            FILE_TO_DELETE = sys.argv[1]

        logger.info(f"准备删除文件: {FILE_TO_DELETE}")
        logger.info(f"目标目录: {TARGET_DIR}\n")

        # ========== 权限校验 ==========
        if not self._is_admin():
            logger.info("当前权限不足，尝试提权...")
            self._run_as_admin()  # 提权后当前进程会退出，新进程将以管理员身份运行

        # ========== 可选：终止相关进程（避免文件被占用）==========
        self._terminate_process_if_exists("easeus.voicewave.exe")
        # 可根据需要添加其他相关进程
        # terminate_process_if_exists("VoiceWave.exe")

        # ========== 执行删除 ==========
        success = self._delete_file_safely(filename)

        if success:
            logger.info("\n操作完成。")
        else:
            logger.error("\n操作失败，请检查日志并重试。")

    def delete_voice_wave_ini(self,backup=True):
        """
        删除 EaseUS VoiceWave 配置文件 VoiceWave.ini
        删除ini文件是为了制造一个新用户启动弹窗展示环境

        Args:
            backup: 是否在删除前创建备份（默认 True）

        Returns:
            bool: 删除成功返回 True，失败返回 False
        """
        # 展开 %APPDATA% 环境变量，获取完整路径
        appdata = os.environ.get('APPDATA')
        if not appdata:
            logger.error("错误: 无法获取 APPDATA 环境变量")
            return False

        ini_path = os.path.join(appdata, 'EaseUS VoiceWave', 'VoiceWave.ini')

        # 检查文件是否存在
        if not os.path.exists(ini_path):
            logger.info(f"提示: 文件不存在: {ini_path}")
            return False

        logger.info(f"目标文件: {ini_path}")

        # 创建备份（可选）
        if backup:
            backup_dir = os.path.join(appdata, 'EaseUS VoiceWave', 'backup')
            os.makedirs(backup_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f'VoiceWave_{timestamp}.ini.bak')

            try:
                shutil.copy2(ini_path, backup_path)
                logger.info(f"已创建备份: {backup_path}")
            except Exception as e:
                logger.warning(f"警告: 备份失败 ({str(e)})，将继续删除原文件")

        # 删除文件
        try:
            os.remove(ini_path)
            logger.info("成功: 文件已删除")
            return True
        except PermissionError:
            logger.error("错误: 权限不足，无法删除文件")
            logger.info("  请尝试以下操作:")
            logger.info("    1. 关闭 EaseUS VoiceWave 程序（检查系统托盘）")
            logger.info("    2. 以管理员身份运行此脚本")
            return False
        except Exception as e:
            logger.error(f"错误: 删除失败: {str(e)}")
            return False

    def modify_time(self, days_offset=-2):
        """
        制造未激活老用户环境，启动弹窗展示问题
        修改INI文件中NEW_USER_LAUNCH_TIME字段的日期值（提前/延后指定天数）
        严格保持文件原始格式：仅替换日期部分，其他所有字符（空格/制表符/换行符）完全不变

        Args:
            days_offset: 日期偏移量（负数=提前，正数=延后），默认-2表示提前2天
        """
        # 获取APPDATA路径
        appdata = os.environ.get('APPDATA')
        if not appdata:
            logger.error("错误: 无法获取 APPDATA 环境变量")
            return False

        file_path = os.path.join(appdata, 'EaseUS VoiceWave', 'VoiceWave.ini')

        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"提示: 文件不存在: {file_path}")
            return False

        logger.info(f"目标文件: {file_path}")

        # 自动检测编码（优先GBK，兼容Windows中文系统）
        encodings = ['gbk', 'utf-8-sig', 'utf-8']
        content = None
        used_encoding = None

        for enc in encodings:
            try:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                content = raw_data.decode(enc)
                used_encoding = enc
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            logger.error("错误: 无法识别文件编码（尝试了GBK/UTF-8）")
            return False

        # 精准正则：捕获完整行结构，仅替换日期部分
        # 模式说明：
        #   ^([ \t]*)                              -> 行首空白（空格/制表符）
        #   (NEW_USER_LAUNCH_TIME)                 -> 字段名
        #   ([ \t]*=[ \t]*)                        -> 等号及周围空白
        #   (\d{4}-\d{2}-\d{2})                    -> 日期（待替换）
        #   ([ \t]+\d{2}:\d{2}:\d{2}[ \t]*)        -> 时间及周围空白
        #   (\r?\n|$)                              -> 换行符或文件结尾
        pattern = r'^([ \t]*)(NEW_USER_LAUNCH_TIME)([ \t]*=[ \t]*)(\d{4}-\d{2}-\d{2})([ \t]+\d{2}:\d{2}:\d{2}[ \t]*)(\r?\n|$)'

        # 查找并替换（仅替换第一个匹配项）
        match = re.search(pattern, content, re.MULTILINE)
        if not match:
            logger.warning("未找到NEW_USER_LAUNCH_TIME字段（或格式不符合预期）")
            return False

        # 提取各部分（完全保留原始字符）
        leading_space = match.group(1)  # 行首空白
        field_name = match.group(2)  # "NEW_USER_LAUNCH_TIME"
        equals_space = match.group(3)  # 等号及周围空白
        old_date = match.group(4)  # 旧日期
        time_part = match.group(5)  # 时间及周围空白
        line_end = match.group(6)  # 换行符或结尾

        try:
            # 计算新日期
            old_dt = datetime.strptime(old_date, "%Y-%m-%d")
            new_dt = old_dt + timedelta(days=days_offset)
            new_date = new_dt.strftime("%Y-%m-%d")

            # 重组行：所有部分原样保留，仅替换日期
            new_line = f"{leading_space}{field_name}{equals_space}{new_date}{time_part}{line_end}"

            # 执行替换（仅替换第一个匹配）
            new_content = re.sub(pattern, new_line, content, count=1, flags=re.MULTILINE)

            # 写回文件（使用原始编码）
            with open(file_path, 'wb') as f:
                f.write(new_content.encode(used_encoding))

            logger.info("修改成功:")
            logger.info(f"  原始日期: {old_date}")
            logger.info(f"  新日期  : {new_date}（{'提前' if days_offset < 0 else '延后'}{abs(days_offset)}天）")
            logger.info(f"  完整行  : {leading_space}{field_name}{equals_space}{new_date}{time_part}")
            return True

        except Exception as e:
            logger.error(f"日期处理错误: {str(e)}")
            return False

    def delete_start_time(self):
        """
        产品设计是每天启动弹窗只弹一次
        删除INI文件中以 START_UP_DISCOUNT_WIDGET_SHOW_TIME=
        保证每次启动都会有弹窗显示
        Args:
            file_path: INI文件完整路径
        """

        # 检查文件是否存在
        # 展开 %APPDATA% 环境变量，获取完整路径
        appdata = os.environ.get('APPDATA')
        if not appdata:
            logger.error("错误: 无法获取 APPDATA 环境变量")
            return False

        file_path = os.path.join(appdata, 'EaseUS VoiceWave', 'VoiceWave.ini')

        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"错误: 文件不存在: {file_path}")
            return False

        # 自动检测编码（优先GBK，兼容Windows中文系统）
        encodings = ['gbk', 'utf-8-sig', 'utf-8']
        raw_content = None
        used_encoding = None
        newline_char = None  # 保留原始换行符风格

        for enc in encodings:
            try:
                # 以二进制读取后解码，便于检测换行符
                with open(file_path, 'rb') as f:
                    raw_bytes = f.read()

                # 检测换行符风格
                if b'\r\n' in raw_bytes:
                    newline_char = '\r\n'
                elif b'\n' in raw_bytes:
                    newline_char = '\n'
                else:
                    newline_char = '\r'

                # 尝试解码
                raw_content = raw_bytes.decode(enc)
                used_encoding = enc
                break
            except (UnicodeDecodeError, AttributeError):
                continue

        if raw_content is None:
            logger.error("错误: 无法识别文件编码（尝试了GBK/UTF-8）")
            return False

        # 按原始换行符分割（保留每行末尾换行符类型）
        if newline_char == '\r\n':
            lines = raw_content.split('\r\n')
            line_sep = '\r\n'
        elif newline_char == '\n':
            lines = raw_content.split('\n')
            line_sep = '\n'
        else:
            lines = raw_content.split('\r')
            line_sep = '\r'

        # 精准匹配：允许行首有空格/制表符，但必须包含目标字段
        # 正则说明: ^[ \t]*START_UP_DISCOUNT_WIDGET_SHOW_TIME[ \t]*=
        pattern = re.compile(r'^[ \t]*START_UP_DISCOUNT_WIDGET_SHOW_TIME[ \t]*=', re.IGNORECASE)

        # 过滤掉匹配的行
        filtered_lines = []
        deleted_count = 0
        deleted_content = None

        for line in lines:
            if pattern.match(line):
                deleted_count += 1
                deleted_content = line
                continue  # 跳过该行（即删除）
            filtered_lines.append(line)

        if deleted_count == 0:
            logger.info("提示: 未找到以 START_UP_DISCOUNT_WIDGET_SHOW_TIME= 开头的行")
            logger.info("  检查项:")
            logger.info("    - 字段名是否完全匹配（注意大小写和下划线）")
            logger.info("    - 行首是否有不可见字符")
            return False

        # 重组内容（使用原始换行符）
        new_content = line_sep.join(filtered_lines)

        # 写回文件（使用原始编码和换行符）
        try:
            with open(file_path, 'w', encoding=used_encoding, newline='') as f:
                f.write(new_content)

            logger.info("成功: 删除完成")
            logger.info(f"  文件路径: {file_path}")
            logger.info(f"  删除行数: {deleted_count}")
            logger.info(f"  删除内容: {deleted_content}")
            logger.info(f"  编码格式: {used_encoding}")
            return True

        except Exception as e:
            logger.error(f"错误: 写入文件失败: {str(e)}")
            logger.info("  请尝试以管理员身份运行脚本")
            return False




    def delete_buy_click_times(self):
        """
        用户进入内购激活弹窗，并且点击buy now 按钮
        删除INI文件中以 CLICK_BUY_CNT=1
        控制了新用户 挽留弹窗的样式不一样


        Args:
            file_path: INI文件完整路径
        """
        # 检查文件是否存在
        # 展开 %APPDATA% 环境变量，获取完整路径
        appdata = os.environ.get('APPDATA')
        if not appdata:
            logger.error("错误: 无法获取 APPDATA 环境变量")
            return False

        file_path = os.path.join(appdata, 'EaseUS VoiceWave', 'VoiceWave.ini')

        if not os.path.exists(file_path):
            logger.error(f"错误: 文件不存在: {file_path}")
            return False

        # 自动检测编码（优先GBK，兼容Windows中文系统）
        encodings = ['gbk', 'utf-8-sig', 'utf-8']
        raw_content = None
        used_encoding = None
        newline_char = None  # 保留原始换行符风格

        for enc in encodings:
            try:
                # 以二进制读取后解码，便于检测换行符
                with open(file_path, 'rb') as f:
                    raw_bytes = f.read()

                # 检测换行符风格
                if b'\r\n' in raw_bytes:
                    newline_char = '\r\n'
                elif b'\n' in raw_bytes:
                    newline_char = '\n'
                else:
                    newline_char = '\r'

                # 尝试解码
                raw_content = raw_bytes.decode(enc)
                used_encoding = enc
                break
            except (UnicodeDecodeError, AttributeError):
                continue

        if raw_content is None:
            logger.error("错误: 无法识别文件编码（尝试了GBK/UTF-8）")
            return False

        # 按原始换行符分割（保留每行末尾换行符类型）
        if newline_char == '\r\n':
            lines = raw_content.split('\r\n')
            line_sep = '\r\n'
        elif newline_char == '\n':
            lines = raw_content.split('\n')
            line_sep = '\n'
        else:
            lines = raw_content.split('\r')
            line_sep = '\r'

        # 精准匹配：允许行首有空格/制表符，但必须包含目标字段
        # 正则说明: ^[ \t]*START_UP_DISCOUNT_WIDGET_SHOW_TIME[ \t]*=
        pattern = re.compile(r'^[ \t]*CLICK_BUY_CNT[ \t]*=', re.IGNORECASE)

        # 过滤掉匹配的行
        filtered_lines = []
        deleted_count = 0
        deleted_content = None

        for line in lines:
            if pattern.match(line):
                deleted_count += 1
                deleted_content = line
                continue  # 跳过该行（即删除）
            filtered_lines.append(line)

        if deleted_count == 0:
            logger.info("提示: 未找到以 CLICK_BUY_CNT= 开头的行")
            logger.info("  检查项:")
            logger.info("    - 字段名是否完全匹配（注意大小写和下划线）")
            logger.info("    - 行首是否有不可见字符")
            return False

        # 重组内容（使用原始换行符）
        new_content = line_sep.join(filtered_lines)

        # 写回文件（使用原始编码和换行符）
        try:
            with open(file_path, 'w', encoding=used_encoding, newline='') as f:
                f.write(new_content)

            logger.info("成功: 删除完成")
            logger.info(f"  文件路径: {file_path}")
            logger.info(f"  删除行数: {deleted_count}")
            logger.info(f"  删除内容: {deleted_content}")
            logger.info(f"  编码格式: {used_encoding}")
            return True

        except Exception as e:
            logger.error(f"错误: 写入文件失败: {str(e)}")
            logger.info("  请尝试以管理员身份运行脚本")
            return False

    import os
    import re

    # def set_show_exit_window_false(self, file_path=None):
    #     r"""
    #     向INI文件添加或更新 SHOW_EXIT_WINDOW=false 配置项
    #     用于控制退出时是否显示确认窗口
    #
    #     Args:
    #         file_path (str, optional): INI文件完整路径。若为None，则使用默认路径：
    #                                    %APPDATA%\EaseUS VoiceWave\VoiceWave.ini
    #
    #     Returns:
    #         bool: 操作成功返回 True，否则返回 False
    #     """
    #     # 确定文件路径（支持环境变量展开）
    #     global operation
    #     if file_path is None:
    #         file_path = r'%APPDATA%\EaseUS VoiceWave\VoiceWave.ini'
    #
    #     expanded_path = os.path.expandvars(file_path)
    #     if not os.path.isabs(expanded_path):
    #         print(f"Error: Expanded path is not absolute: {expanded_path}")
    #         return False
    #
    #     # 检查文件是否存在（不存在则创建空文件）
    #     file_exists = os.path.exists(expanded_path)
    #     if not file_exists:
    #         try:
    #             os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
    #             with open(expanded_path, 'w', encoding='gbk') as f:
    #                 f.write('[Settings]\r\n')
    #             print(f"Info: File not found, created new file: {expanded_path}")
    #         except Exception as e:
    #             print(f"Error: Failed to create file: {str(e)}")
    #             return False
    #
    #     # 读取文件内容（自动检测编码）
    #     encodings = ['gbk', 'utf-8-sig', 'utf-8']
    #     raw_content = None
    #     used_encoding = 'gbk'  # 默认写入编码
    #     newline_char = '\r\n'  # Windows默认换行符
    #
    #     if file_exists:
    #         for enc in encodings:
    #             try:
    #                 with open(expanded_path, 'rb') as f:
    #                     raw_bytes = f.read()
    #
    #                 # 检测换行符风格
    #                 if b'\r\n' in raw_bytes:
    #                     newline_char = '\r\n'
    #                 elif b'\n' in raw_bytes:
    #                     newline_char = '\n'
    #                 else:
    #                     newline_char = '\r'
    #
    #                 raw_content = raw_bytes.decode(enc)
    #                 used_encoding = enc
    #                 break
    #             except (UnicodeDecodeError, AttributeError):
    #                 continue
    #
    #         if raw_content is None:
    #             print("Error: Cannot detect file encoding (tried GBK/UTF-8)")
    #             return False
    #
    #         # 按原始换行符分割
    #         if newline_char == '\r\n':
    #             lines = raw_content.split('\r\n')
    #         elif newline_char == '\n':
    #             lines = raw_content.split('\n')
    #         else:
    #             lines = raw_content.split('\r')
    #     else:
    #         # 新建文件使用默认格式
    #         lines = ['[Settings]']
    #         newline_char = '\r\n'
    #
    #     # 正则匹配配置项（不区分大小写，允许行首空白符）
    #     pattern = re.compile(r'^[ \t]*SHOW_EXIT_WINDOW[ \t]*=', re.IGNORECASE)
    #
    #     # 查找 [Settings] 区段范围
    #     settings_start = None
    #     settings_end = None
    #     in_settings = False
    #
    #     for idx, line in enumerate(lines):
    #         section_match = re.match(r'^\s*\[\s*(\w+)\s*]\s*', line, re.IGNORECASE)
    #         if section_match:
    #             section_name = section_match.group(1).lower()
    #             if section_name == 'settings':
    #                 settings_start = idx
    #                 in_settings = True
    #             elif in_settings:
    #                 settings_end = idx
    #                 in_settings = False
    #         elif in_settings and line.strip() and not line.strip().startswith(';') and not line.strip().startswith('#'):
    #             # 非注释/空行，更新区段结束位置
    #             settings_end = idx + 1
    #
    #     if in_settings:  # 文件以 [Settings] 结尾
    #         settings_end = len(lines)
    #
    #     # 查找并更新现有配置项
    #     updated = False
    #     original_value = None
    #
    #     for idx, line in enumerate(lines):
    #         if pattern.match(line):
    #             # 更新现有行（保留原始缩进）
    #             indent = re.match(r'^[ \t]*', line).group(0) if re.match(r'^[ \t]*', line) else ''
    #             original_value = line.strip()
    #             lines[idx] = f"{indent}SHOW_EXIT_WINDOW=false"
    #             updated = True
    #             operation = "updated"
    #             break
    #
    #     # 未找到配置项，确定插入位置
    #     if not updated:
    #         operation = "added"
    #
    #         # 优先插入到 [Settings] 区段末尾
    #         if settings_end is not None and settings_start is not None:
    #             # 跳过区段末尾的空行
    #             insert_pos = settings_end
    #             while insert_pos > settings_start + 1 and not lines[insert_pos - 1].strip():
    #                 insert_pos -= 1
    #         else:
    #             # 未找到 [Settings]，插入到文件末尾
    #             insert_pos = len(lines)
    #             # 确保前面有空行分隔
    #             if lines and lines[-1].strip():
    #                 lines.append('')
    #                 insert_pos += 1
    #
    #         # 插入新配置项
    #         lines.insert(insert_pos, 'SHOW_EXIT_WINDOW=false')
    #
    #     # 重组内容（使用原始换行符）
    #     line_sep = newline_char
    #     new_content = line_sep.join(lines)
    #
    #     # 写回文件（使用 errors='replace' 避免编码错误）
    #     try:
    #         with open(expanded_path, 'w', encoding=used_encoding, newline='', errors='replace') as f:
    #             f.write(new_content)
    #
    #         print(f"Success: Configuration {operation}")
    #         print(f"  File path: {expanded_path}")
    #         print(f"  Setting: SHOW_EXIT_WINDOW=false")
    #         if original_value:
    #             print(f"  Previous value: {original_value}")
    #         print(f"  Encoding: {used_encoding}")
    #         print(f"  Line ending: {repr(newline_char)}")
    #         return True
    #
    #     except PermissionError:
    #         print("Error: Permission denied")
    #         print("  Please try:")
    #         print("    - Close VoiceWave application if running")
    #         print("    - Run script as Administrator")
    #         return False
    #     except Exception as e:
    #         print(f"Error: Failed to write file: {type(e).__name__}: {str(e)}")
    #         return False

    import os
    import re
    import time

    def set_show_exit_window_false(self,file_path=None):
        r"""
        向INI文件的 [General] 区段添加或更新 SHOW_EXIT_WINDOW=false 配置项
        用于控制退出时是否显示确认窗口

        Args:
            file_path (str, optional): INI文件完整路径。若为None，则使用默认路径：
                                       %APPDATA%\EaseUS VoiceWave\VoiceWave.ini

        Returns:
            bool: 操作成功返回 True，否则返回 False
        """
        # 确定文件路径（支持环境变量展开）
        global operation
        if file_path is None:
            file_path = r'%APPDATA%\EaseUS VoiceWave\VoiceWave.ini'

        expanded_path = os.path.expandvars(file_path)
        if not os.path.isabs(expanded_path):
            logger.error(f"Error: Expanded path is not absolute: {expanded_path}")
            return False

        # 检查文件是否存在（不存在则创建含 [General] 区段的空文件）
        file_exists = os.path.exists(expanded_path)
        if not file_exists:
            try:
                os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
                with open(expanded_path, 'w', encoding='gbk') as f:
                    f.write('[General]\r\n')  # 创建 [General] 区段
                logger.info(f"Info: File not found, created new file with [General] section: {expanded_path}")
            except Exception as e:
                logger.error(f"Error: Failed to create file: {str(e)}")
                return False

        # 读取文件内容（自动检测编码和换行符）
        encodings = ['gbk', 'utf-8-sig', 'utf-8']
        raw_content = None
        used_encoding = 'gbk'
        newline_char = '\r\n'

        if file_exists:
            try:
                with open(expanded_path, 'rb') as f:
                    raw_bytes = f.read()

                # 检测换行符风格
                if b'\r\n' in raw_bytes:
                    newline_char = '\r\n'
                elif b'\n' in raw_bytes:
                    newline_char = '\n'
                else:
                    newline_char = '\r'

                # 尝试解码
                for enc in encodings:
                    try:
                        raw_content = raw_bytes.decode(enc)
                        used_encoding = enc
                        break
                    except UnicodeDecodeError:
                        continue

                if raw_content is None:
                    logger.error("Error: Cannot detect file encoding (tried GBK/UTF-8)")
                    return False

                # 按原始换行符分割
                if newline_char == '\r\n':
                    lines = raw_content.split('\r\n')
                elif newline_char == '\n':
                    lines = raw_content.split('\n')
                else:
                    lines = raw_content.split('\r')
            except Exception as e:
                logger.error(f"Error reading file: {type(e).__name__}: {str(e)}")
                return False
        else:
            # 新建文件使用默认格式
            lines = ['[General]']
            newline_char = '\r\n'

        # 正则：匹配配置项（不区分大小写，允许行首空白）
        pattern = re.compile(r'^[ \t]*SHOW_EXIT_WINDOW[ \t]*=', re.IGNORECASE)

        # 查找 [General] 区段范围（不区分大小写）
        general_start = None
        general_end = None
        in_general = False

        for idx, line in enumerate(lines):
            section_match = re.match(r'^\s*\[\s*(\w+)\s*]\s*', line, re.IGNORECASE)
            if section_match:
                section_name = section_match.group(1).lower()
                if section_name == 'general':
                    general_start = idx
                    in_general = True
                    general_end = idx + 1  # 初始化结束位置
                elif in_general:
                    general_end = idx  # 遇到新区段，结束当前区段
                    in_general = False
            elif in_general:
                # 在 [General] 区段内，更新结束位置（仅对非空/非注释行）
                stripped = line.strip()
                if stripped and not stripped.startswith((';', '#')):
                    general_end = idx + 1

        if in_general:  # 文件以 [General] 结尾
            general_end = len(lines)

        # 情况1: [General] 区段不存在 → 创建区段并插入配置
        if general_start is None:
            logger.info(f"Info: [General] section not found, will be created")
            # 查找插入位置：文件末尾（保持整洁）
            insert_pos = len(lines)
            if lines and lines[-1].strip():  # 末尾非空行，添加空行分隔
                lines.append('')
                insert_pos += 1
            # 插入区段头和配置项
            lines.insert(insert_pos, '[General]')
            lines.insert(insert_pos + 1, 'SHOW_EXIT_WINDOW=false')
            operation = "added (new section)"
            original_value = None
            updated = True
        else:
            # 情况2: [General] 区段存在 → 在区内查找/更新配置
            updated = False
            original_value = None

            # 仅在 [General] 区段范围内搜索（跳过注释/空行）
            search_end = general_end if general_end else len(lines)
            for idx in range(general_start + 1, search_end):
                if pattern.match(lines[idx]):
                    # 更新现有配置（保留原始缩进）
                    indent_match = re.match(r'^[ \t]*', lines[idx])
                    indent = indent_match.group(0) if indent_match else ''
                    original_value = lines[idx].strip()
                    lines[idx] = f"{indent}SHOW_EXIT_WINDOW=false"
                    updated = True
                    operation = "updated"
                    break

            # 未找到配置项 → 插入到区段末尾（跳过末尾空行）
            if not updated:
                insert_pos = general_end if general_end else len(lines)
                # 跳过区段末尾的连续空行
                while insert_pos > general_start + 1 and not lines[insert_pos - 1].strip():
                    insert_pos -= 1

                lines.insert(insert_pos, 'SHOW_EXIT_WINDOW=false')
                operation = "added"
                original_value = None

        # 重组内容（使用原始换行符）
        new_content = newline_char.join(lines)

        # 写回文件（带重试机制应对文件锁定）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if file_exists and attempt > 0:
                    time.sleep(0.5)  # 等待后重试

                with open(expanded_path, 'w', encoding=used_encoding, newline='', errors='replace') as f:
                    f.write(new_content)
                break
            except PermissionError:
                if attempt == max_retries - 1:
                    logger.error("Error: Permission denied (file may be locked by VoiceWave)")
                    logger.info("  Please try:")
                    logger.info("    - Close VoiceWave application completely")
                    logger.info("    - Run script as Administrator")
                    logger.info(f"  File: {expanded_path}")
                    return False
                continue
            except Exception as e:
                logger.error(f"Error writing file: {type(e).__name__}: {str(e)}")
                return False
        else:
            return False  # 重试失败

        # 操作成功反馈
        logger.info(f"Success: Configuration {operation} in [General] section")
        logger.info(f"  File path: {expanded_path}")
        logger.info(f"  Setting: SHOW_EXIT_WINDOW=false")
        if original_value:
            logger.info(f"  Previous value: {original_value}")
        logger.info(f"  Encoding: {used_encoding}")
        logger.info(f"  Line ending: {repr(newline_char)}")
        return True

    import os
    import re
    import time

    def set_close_is_exit(self,file_path=None):
        r"""
        向INI文件的 [General] 区段添加或更新 CLOSE_IS_EXIT=true 配置项
        用于控制关闭窗口时是否直接退出应用（而非最小化到托盘）

        Args:
            file_path (str, optional): INI文件完整路径。若为None，则使用默认路径：
                                       %APPDATA%\EaseUS VoiceWave\VoiceWave.ini

        Returns:
            bool: 操作成功返回 True，否则返回 False
        """
        # 确定文件路径（支持环境变量展开）
        global operation
        if file_path is None:
            file_path = r'%APPDATA%\EaseUS VoiceWave\VoiceWave.ini'

        expanded_path = os.path.expandvars(file_path)
        if not os.path.isabs(expanded_path):
            logger.error(f"Error: Expanded path is not absolute: {expanded_path}")
            return False

        # 检查文件是否存在（不存在则创建含 [General] 区段的空文件）
        file_exists = os.path.exists(expanded_path)
        if not file_exists:
            try:
                os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
                with open(expanded_path, 'w', encoding='gbk') as f:
                    f.write('[General]\r\n')
                logger.info(f"Info: File not found, created new file with [General] section: {expanded_path}")
            except Exception as e:
                logger.error(f"Error: Failed to create file: {str(e)}")
                return False

        # 读取文件内容（自动检测编码和换行符）
        encodings = ['gbk', 'utf-8-sig', 'utf-8']
        raw_content = None
        used_encoding = 'gbk'
        newline_char = '\r\n'

        if file_exists:
            try:
                with open(expanded_path, 'rb') as f:
                    raw_bytes = f.read()

                # 检测换行符风格
                if b'\r\n' in raw_bytes:
                    newline_char = '\r\n'
                elif b'\n' in raw_bytes:
                    newline_char = '\n'
                else:
                    newline_char = '\r'

                # 尝试解码
                for enc in encodings:
                    try:
                        raw_content = raw_bytes.decode(enc)
                        used_encoding = enc
                        break
                    except UnicodeDecodeError:
                        continue

                if raw_content is None:
                    logger.error("Error: Cannot detect file encoding (tried GBK/UTF-8)")
                    return False

                # 按原始换行符分割
                if newline_char == '\r\n':
                    lines = raw_content.split('\r\n')
                elif newline_char == '\n':
                    lines = raw_content.split('\n')
                else:
                    lines = raw_content.split('\r')
            except Exception as e:
                logger.error(f"Error reading file: {type(e).__name__}: {str(e)}")
                return False
        else:
            # 新建文件使用默认格式
            lines = ['[General]']
            newline_char = '\r\n'

        # 正则：匹配配置项（不区分大小写，允许行首空白）
        pattern = re.compile(r'^[ \t]*CLOSE_IS_EXIT[ \t]*=', re.IGNORECASE)

        # 查找 [General] 区段范围（不区分大小写）
        general_start = None
        general_end = None
        in_general = False

        for idx, line in enumerate(lines):
            section_match = re.match(r'^\s*\[\s*(\w+)\s*]\s*', line, re.IGNORECASE)
            if section_match:
                section_name = section_match.group(1).lower()
                if section_name == 'general':
                    general_start = idx
                    in_general = True
                    general_end = idx + 1
                elif in_general:
                    general_end = idx
                    in_general = False
            elif in_general:
                stripped = line.strip()
                if stripped and not stripped.startswith((';', '#')):
                    general_end = idx + 1

        if in_general:  # 文件以 [General] 结尾
            general_end = len(lines)

        # 情况1: [General] 区段不存在 → 创建区段并插入配置
        if general_start is None:
            logger.info(f"Info: [General] section not found, will be created")
            insert_pos = len(lines)
            if lines and lines[-1].strip():
                lines.append('')
                insert_pos += 1
            lines.insert(insert_pos, '[General]')
            lines.insert(insert_pos + 1, 'CLOSE_IS_EXIT=true')
            operation = "added (new section)"
            original_value = None
            updated = True
        else:
            # 情况2: [General] 区段存在 → 在区内查找/更新配置
            updated = False
            original_value = None

            search_end = general_end if general_end else len(lines)
            for idx in range(general_start + 1, search_end):
                if pattern.match(lines[idx]):
                    indent_match = re.match(r'^[ \t]*', lines[idx])
                    indent = indent_match.group(0) if indent_match else ''
                    original_value = lines[idx].strip()
                    lines[idx] = f"{indent}CLOSE_IS_EXIT=true"
                    updated = True
                    operation = "updated"
                    break

            # 未找到配置项 → 插入到区段末尾
            if not updated:
                insert_pos = general_end if general_end else len(lines)
                while insert_pos > general_start + 1 and not lines[insert_pos - 1].strip():
                    insert_pos -= 1

                lines.insert(insert_pos, 'CLOSE_IS_EXIT=true')
                operation = "added"
                original_value = None

        # 重组内容（使用原始换行符）
        new_content = newline_char.join(lines)

        # 写回文件（带重试机制）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if file_exists and attempt > 0:
                    time.sleep(0.5)

                with open(expanded_path, 'w', encoding=used_encoding, newline='', errors='replace') as f:
                    f.write(new_content)
                break
            except PermissionError:
                if attempt == max_retries - 1:
                    logger.error("Error: Permission denied (file may be locked by VoiceWave)")
                    logger.info("  Please try:")
                    logger.info("    - Close VoiceWave application completely")
                    logger.info("    - Run script as Administrator")
                    logger.info(f"  File: {expanded_path}")
                    return False
                continue
            except Exception as e:
                logger.error(f"Error writing file: {type(e).__name__}: {str(e)}")
                return False
        else:
            return False

        # 操作成功反馈
        logger.info(f"Success: Configuration {operation} in [General] section")
        logger.info(f"  File path: {expanded_path}")
        logger.info(f"  Setting: CLOSE_IS_EXIT=true")
        if original_value:
            logger.info(f"  Previous value: {original_value}")
        logger.info(f"  Encoding: {used_encoding}")
        logger.info(f"  Line ending: {repr(newline_char)}")
        return True

# ==================== 使用示例 ====================
if __name__ == "__main__":

    # 创建管理器实例（可自定义等待时间和自动提权行为）

    manager = ConfigManager()

    success = manager.set_close_is_exit()

    logger.info(success)



