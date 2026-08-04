#!/usr/bin/python3
# -*- coding : utf-8 -*-
# @Author : leikaifu
# @email :  leikaifu@info.easeus.com.cn

import os
import subprocess
import hashlib
from pathlib import Path
from commons.utils.myLogging import get_logger

# ======================
# 配置区（请按实际修改）
# ======================

# 远程 SMB 共享信息
REMOTE_HOST = r"\\10.2.53.110"
REMOTE_SHARE = r"公司交换区"
REMOTE_SUB_PATH = r"Z_张雯\ertvc_v2.1文件"  # ← 确认此路径真实存在

# 本地 ONNX 文件目录
LOCAL_DIR = r"C:\ProgramData\EaseUS\VoiceWave\ai\voices_onnx_ertvc2"

# 账号密码（直接填写）
USERNAME = "leikaifu@info.easeus.com.cn"
PASSWORD = "yiwodisk123!!!"

# 是否在结束时断开连接
DISCONNECT_AFTER = False

logger = get_logger()

# ======================
# 工具函数
# ======================

def calculate_md5(file_path: str) -> str:
    """计算文件 MD5，失败返回 None"""
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (OSError, IOError) as e:
        logger.error(f"读取文件失败: {file_path} | 错误: {e}")
        return None

def get_local_onnx_files(folder: str):
    """获取本地所有 .onnx 文件"""
    path = Path(folder)
    if not path.exists():
        raise FileNotFoundError(f"本地目录不存在: {folder}")
    return [f.resolve() for f in path.glob("*.onnx") if f.is_file()]

def build_remote_mapping(folder: str):
    """构建远程 ONNX 文件映射 {stem: absolute_path}"""
    path = Path(folder)
    if not path.exists():
        raise FileNotFoundError(f"远程目录不存在: {folder}")
    mapping = {}
    for f in path.glob("*.onnx"):
        if f.is_file():
            mapping[f.stem] = str(f.resolve())
    return mapping

def compare_by_prefix_v2(local_dir: str, remote_dir: str):
    """对比本地 xxx.onnx 与远程 xxx_*.onnx 的 MD5"""
    logger.info("正在加载本地 ONNX 文件...")
    try:
        local_files = get_local_onnx_files(local_dir)
    except Exception as e:
        logger.error(f"本地路径错误: {e}")
        return False

    logger.info("正在加载远程 ONNX 文件...")
    try:
        remote_map = build_remote_mapping(remote_dir)
    except Exception as e:
        logger.error(f"远程路径错误: {e}")
        return False

    matched_pairs = []
    remote_stems = list(remote_map.keys())

    for local_file in local_files:
        local_stem = local_file.stem
        expected_prefix = local_stem + "_"

        found = False
        for remote_stem in remote_stems:
            if remote_stem.startswith(expected_prefix):
                matched_pairs.append({
                    "local_path": str(local_file),
                    "remote_path": remote_map[remote_stem],
                    "prefix": local_stem
                })
                found = True
                break

        if not found:
            logger.warning(f"未找到匹配的远程文件: {local_stem}.onnx")

    if not matched_pairs:
        logger.warning("未找到任何匹配的文件对。")
        return False

    logger.info(f"共找到 {len(matched_pairs)} 对匹配文件，开始 MD5 对比...")

    mismatches = []
    for pair in matched_pairs:
        local_md5 = calculate_md5(pair["local_path"])
        remote_md5 = calculate_md5(pair["remote_path"])

        if local_md5 is None or remote_md5 is None:
            logger.warning(f"跳过无法读取的文件对: 编号 {pair['prefix']}")
            continue

        if local_md5 != remote_md5:
            mismatches.append({
                "prefix": pair["prefix"],
                "local_path": pair["local_path"],
                "remote_path": pair["remote_path"],
                "local_md5": local_md5,
                "remote_md5": remote_md5
            })

    if not mismatches:
        logger.info("\n对比通过：所有匹配的 ONNX 文件 MD5 值一致。")
        return True
    else:
        logger.warning(f"\n对比结果前后MD5不一致说明声纹数据已经加密：共发现 {len(mismatches)} 个不一致的文件：")
        for item in mismatches:
            logger.warning(f"\n编号: {item['prefix']}")
            logger.warning(f"  本地文件: {os.path.basename(item['local_path'])}")
            logger.warning(f"  远程文件: {os.path.basename(item['remote_path'])}")
            logger.warning(f"  本地 MD5: {item['local_md5']}")
            logger.warning(f"  远程 MD5: {item['remote_md5']}")
        return False

# >>> 以下 connect / disconnect 函数保持不变（已包含在下方）<<<

def connect_remote_share():
    """安全连接远程共享（避免编码崩溃）"""
    full_unc = f"{REMOTE_HOST}\\{REMOTE_SHARE}"
    target_path = f"{full_unc}\\{REMOTE_SUB_PATH}"

    try:
        result = subprocess.run(["net", "use"], capture_output=True)
        try:
            output = result.stdout.decode('gbk')
        except UnicodeDecodeError:
            try:
                output = result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                output = result.stdout.decode('utf-8', errors='replace')
        if full_unc.lower() in output.lower():
            logger.info("共享已连接，跳过登录。")
            return target_path
    except Exception as e:
        logger.error(f"检查现有连接时出错: {e}")

    if not USERNAME or not PASSWORD:
        logger.error("错误：USERNAME 或 PASSWORD 未设置。")
        return None

    logger.info(f"正在连接远程共享: {full_unc}")
    cmd = ["net", "use", full_unc, f"/user:{USERNAME}", PASSWORD]
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode == 0:
        logger.info("远程共享连接成功。")
        return target_path
    else:
        try:
            stderr_msg = result.stderr.decode('gbk')
        except UnicodeDecodeError:
            try:
                stderr_msg = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                stderr_msg = result.stderr.decode('utf-8', errors='replace')
        logger.error(f"net use 失败: {stderr_msg.strip()}")
        return None

def disconnect_remote_share():
    """断开远程共享（安全执行）"""
    full_unc = f"{REMOTE_HOST}\\{REMOTE_SHARE}"
    try:
        subprocess.run(["net", "use", full_unc, "/delete"], capture_output=True)
        logger.info("已尝试断开远程共享连接。")
    except Exception as e:
        logger.error(f"断开连接时出错: {e}")

# ======================
# 主程序
# ======================

def main():
    remote_dir = connect_remote_share()
    if not remote_dir:
        return False

    if not os.path.exists(remote_dir):
        logger.error(f"远程路径不存在: {remote_dir}")
        if DISCONNECT_AFTER:
            disconnect_remote_share()
        return False

    success = compare_by_prefix_v2(LOCAL_DIR, remote_dir)

    if DISCONNECT_AFTER:
        disconnect_remote_share()

    return success

if __name__ == "__main__":
    success = main()
