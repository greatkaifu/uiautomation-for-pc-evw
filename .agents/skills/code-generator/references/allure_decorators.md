# Allure 装饰器分层规范

## 分工表

| 装饰器 | Allure 层级 | 用途 | 示例 |
|--------|------------|------|------|
| `@allure.epic` | Epic | 产品/项目级别 | `@allure.epic("PC 客户端")` |
| `@allure.feature` | Feature | 功能模块 | `@allure.feature("Login")` |
| `@allure.story` | Story | 场景分组 | `@allure.story("用户正常登录")` |
| `@allure.title` | Title | 单个用例验证点 | `@allure.title("验证用户使用正确凭据可以成功登录")` |

## 装饰器放置位置

- `@allure.epic` 和 `@allure.feature` 放在**测试类**上
- `@allure.story` 和 `@allure.title` 放在**测试方法**上

## 使用规范

- `@allure.epic` 固定为 `"PC 客户端"`
- `@allure.feature` 与测试类名保持一致，如 `TestLogin` → `@allure.feature("Login")`
- `@allure.story` 按功能模块命名，如 `"克隆音效"`、`"文件变声-导入"`、`"设置页-设备选择"`
- `@allure.title` 用一句完整中文描述验证点，包含「操作 + 预期结果」：
  - ✅ `@allure.title("点击nav5声音克隆菜单切换正常")`
  - ✅ `@allure.title("导入视频无音频流文件，弹出提示导入失败弹窗")`
  - ❌ `@allure.title("克隆音效")`（与 story 重复，没有具体验证点）

## 测试方法装饰器顺序

```python
@pytest.mark.test
@allure.story("场景分组")
@allure.title("操作+预期结果")
@pytest.mark.dependency(name="test_xxx")
def test_xxx(self, window):
    pass
```
