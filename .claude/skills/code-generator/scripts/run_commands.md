# 常用执行命令

## 运行标记为 test 的用例（调试/执行时使用）
```bash
pytest -v -s -m test
```

## 运行指定测试文件
```bash
pytest testcase/test_xxx.py -v -s -m test
```

## 执行所有用例
```bash
pytest testcase/
```

## 生成测试报告数据（执行用例并输出 Allure 原始数据）
```bash
pytest testcase/ --alluredir=allure-results --clean-alluredir -v
```

## Allure 报告规则

当用户提示词中包含 **"生成报告"**、**"打开报告"** 或 **"查看报告"** 时，按以下流程处理：

### 第一步：检查是否有 Allure 报告数据

检查项目根目录下 `allure-results/` 目录是否存在且非空：
```bash
ls allure-results/
```

如果 `allure-results/` 不存在或为空（无数据），告知用户本地没有报告数据，需要先执行测试用例生成数据，然后生成报告：
```bash
pytest testcase/ --alluredir=allure-results --clean-alluredir -v
allure generate -o report -c allure-results/
```
之后跳到第三步启动服务。

### 第二步：判断测试数据是否有更新

对比 `allure-results/` 目录中最新文件的修改时间与 `report/` 目录的生成时间：
```bash
# 获取 allure-results 中最新文件的修改时间
python -c "import os; print(max(os.path.getmtime(os.path.join('allure-results',f)) for f in os.listdir('allure-results')))"
# 获取 report 目录的生成时间
python -c "import os; print(os.path.getmtime('report'))"
```

#### 情况 A：测试数据有更新（allure-results 最新文件时间 > report 目录时间）

说明测试数据发生了变更，需要重新生成报告：
```bash
allure generate -o report -c allure-results/
```

#### 情况 B：测试数据没有更新（allure-results 最新文件时间 <= report 目录时间）

说明报告已是最新，**跳过报告生成步骤**，直接进入第三步启动服务查看。

### 第三步：启动服务打开报告

⚠️ **禁止直接用浏览器打开 `report/index.html`**，必须通过 `allure open` 启动本地 HTTP 服务器来打开报告，否则浏览器会因跨域限制无法加载 JSON 数据。

```bash
allure open report
```

该命令会启动本地 HTTP 服务器并自动打开浏览器，无需再手动执行 `start` 命令。
仅在浏览器未自动打开时，才使用系统命令手动打开：
```bash
start http://127.0.0.1:xxxxx
```

## 按标记运行
```bash
pytest -m "ui" -v
```