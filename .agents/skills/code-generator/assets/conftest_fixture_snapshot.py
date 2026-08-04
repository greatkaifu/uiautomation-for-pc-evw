 # conftest.py Fixture 快照
# 本文件提取了 conftest.py 中所有可用的 fixture 签名和文档，
# 供 skill 生成测试代码时参考，自动选用正确的 fixture。

"""
======================================
fixture 列表与用法
======================================

1. active_window (scope="module")
   - 用途: 已激活用户环境，整个测试模块执行一次
   - 返回: main_window (uiautomation.WindowControl)
   - 行为: 启动程序 → 获取主窗口 → yield → 无后置清理（不关闭程序）
   - 适用: 激活状态下的功能测试

2. active_window_function (scope="function")
   - 用途: 已激活用户环境，每个测试用例执行一次
   - 返回: main_window
   - 行为: 启动程序 → yield → 关闭程序 + kill_process
   - 适用: 需要每个用例前后重启的激活状态测试

3. window (scope="module")
   - 用途: 删除ini配置文件后的初始状态环境
   - 返回: main_window
   - 行为: 删除ini → 启动程序 → set_show_exit_window_false → yield → CloseProgram + kill
   - 适用: 关闭程序流程测试

4. bottom_window (scope="function")
   - 用途: 删除ini后的初始状态环境（function级别）
   - 返回: main_window
   - 行为: 删除ini → 启动 → yield → CloseProgram + select_exit_way + click_ok + kill
   - 适用: 底部栏流程测试

5. main_window (scope="class")
   - 用途: 未激活新用户环境
   - 返回: main_window
   - 行为: 删除ini + 删除激活bin → 启动 → yield → 关闭启动弹窗 + CloseProgram + select_exit_way + click_ok + kill
   - 适用: 未激活新用户功能测试

6. new_main_window (scope="class")
   - 用途: 未激活新用户环境（删除ini）
   - 返回: main_window
   - 行为: 删除ini → 启动 → yield → CloseProgram + select_exit_way + click_ok + kill

7. old_main_window (scope="function")
   - 用途: 未激活老用户环境（修改时间 + 删除start_time）
   - 返回: main_window
   - 行为: kill进程 → modify_time + delete_start_time → 启动 → yield → select_exit_way + click_ok + kill
   - 适用: 老用户启动弹窗测试

8. Inactive_main_window (scope="function")
   - 用途: 未激活用户环境（删除激活bin + ini）
   - 返回: main_window
   - 行为: kill进程 → 删除激活bin + ini → 启动 → yield → select_exit_way + click_ok + kill

9. newuser_language_window (scope="function", params=["English"])
   - 用途: 未激活新用户 + 指定语言环境
   - 返回: (main_window, language_param)
   - 行为: 配置ini → 切换注册表语言 → 启动 → yield → kill
   - 适用: 多语言新用户测试

10. olduser_language_window (scope="function", params=["English"])
    - 用途: 未激活老用户 + 指定语言环境
    - 返回: (main_window, language_param)
    - 行为: modify_time + delete_start_time → 切换语言 → 启动 → yield → kill
    - 适用: 多语言老用户测试

11. creation_language_window (scope="function", params=["Japanese","ChineseTrad","ChineseSimp","Spanish","Turkish","Arabic"])
    - 用途: 声音克隆功能多语言环境
    - 返回: (main_window, language_param)
    - 行为: 配置ini → 切换语言 → 启动 → yield → kill

12. login_window (scope="function")
    - 用途: 未激活新用户登录环境
    - 返回: main_window
    - 行为: 删除ini → 启动 → yield → 无后置清理
    - 适用: 登录功能测试

======================================
常用 fixture 选择指南
======================================

| 测试场景 | 推荐 fixture | 返回值 |
|----------|-------------|--------|
| 激活用户功能测试 | active_window | main_window |
| 需隔离的激活用户测试 | active_window_function | main_window |
| 未激活新用户测试 | main_window | main_window |
| 未激活老用户启动弹窗 | old_main_window | main_window |
| 关闭程序流程 | window | main_window |
| 登录功能 | login_window | main_window |
| 多语言新用户 | newuser_language_window | (main_window, lang) |
| 多语言老用户 | olduser_language_window | (main_window, lang) |
| 多语言克隆功能 | creation_language_window | (main_window, lang) |
"""
