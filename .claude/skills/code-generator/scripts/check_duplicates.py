#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查项目中是否存在重复的文件名、类名和方法名。

用法：
    python check_duplicates.py [path]

path 可以是项目根目录。默认为当前脚本的上级项目根目录。

检查项：
    1. testcase/ 下重复的测试文件名
    2. pom/ 下重复的 POM 文件名
    3. 同一测试文件中重复的测试类名
    4. 同一 POM 文件中重复的 POM 类名
    5. 同一类中重复的方法名（包含 POM 方法和 test_* 方法）
    6. 跨文件重复的测试类名、POM 类名
"""
import ast
import os
import sys
from collections import defaultdict
from pathlib import Path


def find_files(root, pattern):
    """递归查找匹配模式的文件，返回相对路径列表。"""
    return sorted([str(p.relative_to(root)) for p in Path(root).rglob(pattern)])


def check_duplicate_file_names(root, rel_paths):
    """检查相对路径列表中是否有同名文件。"""
    name_map = defaultdict(list)
    for p in rel_paths:
        name_map[Path(p).name].append(p)
    return {name: paths for name, paths in name_map.items() if len(paths) > 1}


def extract_classes_and_methods(file_path):
    """解析单个 Python 文件，返回类名列表和每个类的方法名列表。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except SyntaxError as e:
        print(f"[语法错误] {file_path}: {e}")
        return [], {}

    classes = []
    methods_per_class = defaultdict(list)

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods_per_class[node.name].append(item.name)

    return classes, dict(methods_per_class)


def check_duplicate_classes(file_paths):
    """检查跨文件重复的类名。"""
    class_map = defaultdict(list)
    for fp in file_paths:
        classes, _ = extract_classes_and_methods(fp)
        for cls in classes:
            class_map[cls].append(fp)
    return {cls: paths for cls, paths in class_map.items() if len(paths) > 1}


def check_duplicate_methods_in_classes(file_paths):
    """检查同一类中重复的方法名。"""
    duplicates = []
    for fp in file_paths:
        _, methods_per_class = extract_classes_and_methods(fp)
        for cls, methods in methods_per_class.items():
            seen = defaultdict(int)
            for m in methods:
                seen[m] += 1
            for m, count in seen.items():
                if count > 1:
                    duplicates.append(f"{fp}:{cls}.{m}（出现 {count} 次）")
    return duplicates


def check_duplicate_classes_in_file(file_paths):
    """检查同一文件中重复的类名。"""
    duplicates = []
    for fp in file_paths:
        classes, _ = extract_classes_and_methods(fp)
        seen = defaultdict(int)
        for c in classes:
            seen[c] += 1
        for c, count in seen.items():
            if count > 1:
                duplicates.append(f"{fp}:{c}（出现 {count} 次）")
    return duplicates


def check_project(target_root):
    """对项目执行全部重复检查并打印结果。"""
    testcase_dir = Path(target_root) / "testcase"
    pom_dir = Path(target_root) / "pom"

    test_files = []
    pom_files = []
    if testcase_dir.exists():
        test_files = sorted(testcase_dir.glob("test_*.py"))
    if pom_dir.exists():
        pom_files = sorted(pom_dir.glob("voicewave_*.py"))

    issues = []

    # 1. 重复文件名
    test_file_dups = check_duplicate_file_names(target_root, [str(p.relative_to(target_root)) for p in test_files])
    if test_file_dups:
        issues.append("测试文件名重复：")
        for name, paths in test_file_dups.items():
            issues.append(f"  {name}: {', '.join(paths)}")

    pom_file_dups = check_duplicate_file_names(target_root, [str(p.relative_to(target_root)) for p in pom_files])
    if pom_file_dups:
        issues.append("POM 文件名重复：")
        for name, paths in pom_file_dups.items():
            issues.append(f"  {name}: {', '.join(paths)}")

    # 2. 同一文件中重复类名
    all_py_files = test_files + pom_files
    class_in_file_dups = check_duplicate_classes_in_file(all_py_files)
    if class_in_file_dups:
        issues.append("同一文件中类名重复：")
        for item in class_in_file_dups:
            issues.append(f"  {item}")

    # 3. 跨文件重复类名
    class_dups = check_duplicate_classes(all_py_files)
    if class_dups:
        issues.append("跨文件类名重复：")
        for cls, paths in class_dups.items():
            issues.append(f"  {cls}: {', '.join(paths)}")

    # 4. 同一类中重复方法名
    method_dups = check_duplicate_methods_in_classes(all_py_files)
    if method_dups:
        issues.append("同一类中方法名重复：")
        for item in method_dups:
            issues.append(f"  {item}")

    if issues:
        print("发现以下命名重复问题，请修复：")
        for issue in issues:
            print(issue)
        sys.exit(1)
    else:
        print("命名唯一性检查通过，未发现重复的文件名、类名或方法名。")


if __name__ == "__main__":
    default_root = Path(__file__).resolve().parents[2]
    target = sys.argv[1] if len(sys.argv) > 1 else str(default_root)
    if not Path(target).is_dir():
        print(f"路径不存在或不是目录: {target}")
        sys.exit(1)
    check_project(target)
