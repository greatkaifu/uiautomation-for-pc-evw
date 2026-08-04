# -*- coding: utf-8 -*-
"""
文件归类工具
遍历指定目录下的所有子文件夹，将文件归类到一个目标文件夹中。
支持处理文件名冲突（自动重命名）。
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from commons.utils.myLogging import get_logger

logger = get_logger()


def organize_files(
    source_dir: str,
    target_dir: Optional[str] = None,
    operation: str = "copy",
    rename_on_conflict: bool = True,
    preserve_structure: bool = False,
) -> dict:
    """
    遍历 source_dir 下的所有子文件夹，将文件归类到目标文件夹中。

    Args:
        source_dir: 源目录路径
        target_dir: 目标目录路径，默认为 source_dir 同级目录下的 organized 文件夹
        operation: 操作类型，"copy" 复制 或 "move" 移动
        rename_on_conflict: 遇到文件名冲突时是否自动重命名
        preserve_structure: 是否保留子目录结构（False 则平铺到同一目录）

    Returns:
        dict: 包含处理结果统计信息
            {
                "total_files": 总文件数,
                "success": 成功数,
                "failed": 失败数,
                "skipped": 跳过数,
                "errors": 错误列表
            }
    """
    source_path = Path(source_dir).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"源目录不存在: {source_dir}")

    if target_dir is None:
        target_path = source_path.parent / f"{source_path.name}_organized"
    else:
        target_path = Path(target_dir).resolve()

    target_path.mkdir(parents=True, exist_ok=True)

    result = {
        "total_files": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "errors": [],
    }

    # 收集所有文件（排除目标目录本身）
    all_files = []
    for root, dirs, files in os.walk(source_path):
        # 跳过目标目录，避免递归处理
        if target_path in Path(root).parents or Path(root) == target_path:
            continue
        for file in files:
            all_files.append(Path(root) / file)

    result["total_files"] = len(all_files)

    for file_path in all_files:
        try:
            if preserve_structure:
                # 保留相对目录结构
                relative_dir = file_path.parent.relative_to(source_path)
                dest_dir = target_path / relative_dir
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / file_path.name
            else:
                # 平铺到同一目录
                dest_file = target_path / file_path.name

            # 处理文件名冲突
            if dest_file.exists() and rename_on_conflict and not preserve_structure:
                stem = dest_file.stem
                suffix = dest_file.suffix
                counter = 1
                while dest_file.exists():
                    dest_file = target_path / f"{stem}_{counter:03d}{suffix}"
                    counter += 1

            # 执行复制或移动
            if operation == "copy":
                shutil.copy2(file_path, dest_file)
            elif operation == "move":
                shutil.move(str(file_path), str(dest_file))
            else:
                raise ValueError(f"不支持的操作类型: {operation}，请使用 'copy' 或 'move'")

            result["success"] += 1
        except Exception as e:
            result["failed"] += 1
            result["errors"].append(f"{file_path}: {e}")

    return result


def organize_subfolders_flat(source_dir: str, target_dir: Optional[str] = None) -> dict:
    """
    将 source_dir 下每个子文件夹中的文件平铺归类到一个统一文件夹中。
    自动处理文件名冲突。

    Args:
        source_dir: 源目录路径（如 language_screenshots/克隆中页）
        target_dir: 目标目录路径，默认在 source_dir 同级创建 *_flat 目录

    Returns:
        dict: 处理结果统计
    """
    source_path = Path(source_dir).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"源目录不存在: {source_dir}")

    if target_dir is None:
        target_path = source_path.parent / f"{source_path.name}_flat"
    else:
        target_path = Path(target_dir).resolve()

    target_path.mkdir(parents=True, exist_ok=True)

    result = {
        "total_files": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "errors": [],
        "target_dir": str(target_path),
    }

    # 只遍历 source_dir 下的直接子文件夹
    for subdir in sorted(source_path.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir == target_path:
            continue

        for file_path in subdir.iterdir():
            if not file_path.is_file():
                continue

            result["total_files"] += 1
            try:
                dest_file = target_path / file_path.name

                # 处理文件名冲突
                if dest_file.exists():
                    stem = dest_file.stem
                    suffix = dest_file.suffix
                    counter = 1
                    while dest_file.exists():
                        dest_file = target_path / f"{stem}_{counter:03d}{suffix}"
                        counter += 1

                shutil.copy2(file_path, dest_file)
                result["success"] += 1
            except Exception as e:
                result["failed"] += 1
                result["errors"].append(f"{file_path}: {e}")

    return result


if __name__ == "__main__":
    # 示例用法
    import json

    # 示例 1: 将指定目录下所有子文件夹中的文件平铺归类
    source = r"C:\Users\admin\Desktop\多语言\导入功能"
    logger.info(f"正在处理: {source}")
    result = organize_subfolders_flat(source)
    logger.info(json.dumps(result, ensure_ascii=False, indent=2))

    # 示例 2: 完整递归归类（包含更深层次的子目录）
    # result = organize_files(
    #     source_dir="language_screenshots",
    #     target_dir="language_screenshots_organized",
    #     operation="copy",
    #     rename_on_conflict=True,
    # )
    # print(json.dumps(result, ensure_ascii=False, indent=2))
