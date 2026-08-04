#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查测试文件中是否存在无断言的 test_* 函数。

用法：
    python check_assertions.py [path]

path 可以是单个测试文件或目录。默认为 ../../testcase/

检查规则（满足任一即视为有断言）：
    1. 函数体内包含 assert 语句
    2. 函数体内调用 control_raise(...) 或 element_raise(...)
    3. 函数体内调用其他 pytest 可识别为失败的异常抛出（如 pytest.xxx）
"""
import ast
import os
import sys
from pathlib import Path


# 视为断言的调用名称
ASSERTION_CALL_NAMES = {
    "control_raise",
    "element_raise",
    "pytest.fail",
    "pytest.xfail",
    "pytest.skip",
    "fail",
    "xfail",
    "skip",
}


def _is_assertion_call(node):
    """判断一个调用节点是否属于断言类调用。"""
    if isinstance(node.func, ast.Name):
        return node.func.id in ASSERTION_CALL_NAMES
    if isinstance(node.func, ast.Attribute):
        # 处理 module.func 形式，如 pytest.fail
        full_name = getattr(node.func, "attr", "")
        parent = node.func.value
        if isinstance(parent, ast.Name):
            full_name = f"{parent.id}.{full_name}"
        return full_name in ASSERTION_CALL_NAMES
    return False


def _has_assertion(node):
    """递归检查节点及其子树是否包含断言。"""
    for child in ast.walk(node):
        if isinstance(child, ast.Assert):
            return True
        if isinstance(child, ast.Call) and _is_assertion_call(child):
            return True
    return False


def check_file(file_path):
    """检查单个测试文件，返回无断言的 test_* 方法列表。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except SyntaxError as e:
        print(f"[语法错误] {file_path}: {e}")
        return []

    missing = []
    for class_node in tree.body:
        if not isinstance(class_node, ast.ClassDef):
            continue
        for func_node in class_node.body:
            if not isinstance(func_node, ast.FunctionDef):
                continue
            if not func_node.name.startswith("test_"):
                continue
            if not _has_assertion(func_node):
                missing.append(f"{class_node.name}.{func_node.name}")
    return missing


def check_path(target_path):
    """检查路径（文件或目录），打印结果。"""
    target = Path(target_path)
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(target.glob("test_*.py"))
    else:
        print(f"路径不存在: {target_path}")
        sys.exit(1)

    all_missing = []
    for file_path in files:
        missing = check_file(file_path)
        if missing:
            all_missing.extend(f"{file_path}:{m}" for m in missing)

    if all_missing:
        print("发现以下测试用例没有断言，请补充 assert 或 control_raise/element_raise：")
        for item in all_missing:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print("断言检查通过，所有 test_* 函数均包含断言。")


if __name__ == "__main__":
    default_path = Path(__file__).resolve().parents[2] / "testcase"
    target = sys.argv[1] if len(sys.argv) > 1 else str(default_path)
    check_path(target)
