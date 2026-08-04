# 常用 API 速查

## 一、图像/图标操作（BasePage 方法）

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| 图像点击 | `self.find_element_and_click(template_path, timeout=None)` | 查找并点击图像，timeout=None即不等待只查找一次 |
| 图像检查 | `self.find_element(template_path, timeout=None)` | 检查图像是否存在，找到返回 `True`，未找到返回 `False`；timeout=None则使用类里面默认的超时 |
| 图像异常 | `element_raise(template_path, description, timeout)` | 图像必须存在，否则抛 `TargetElementNotFoundError` |
| 相对点击 | `self.click_relative_to_element(template_path, offset_x, offset_y, timeout=None)` | 相对图像偏移点击，timeout=None即不等待只查找一次 |
| 图像输入 | `self.find_element_and_input(template_path, content, timeout=None)` | 查找图像元素并输入内容 |
| 鼠标悬停 | `self.hover_to_element(template_path, timeout=None)` | 移动鼠标到图像位置，不存在抛 `TargetElementNotFoundError` |
| 发送内容 | `self.send_to_contents(template_path, str_content, offset_x, offset_y, timeout=None)` | 相对图像偏移位置发送内容，不存在抛 `TargetElementNotFoundError` |
| 图像滚动查找 | `self.find_element_by_scroll_up_and_down(template_path, max_scroll_down, max_scroll_up)` | 通过滚动查找图像/图标，找到返回 `True`，未找到返回 `None` |
| 图像单向滚动查找 | `self.find_element_by_scroll(template_path, max_scroll_count, scroll_direction, scroll_interval)` | 单方向（上或下）滚动查找图像或图标，找到返回 `True`，未找到返回 `None` |
| 等待图像出现 | `self.wait_for_image_appear(image_path, timeout=30)` | 在规定时间内等待图像出现，出现返回 `True`，超时返回 `False` |
| 等待图像消失 | `self.wait_for_image_disappear(image_path, timeout=10)` | 在规定时间内等待图像消失，消失返回 `True`，超时返回 `False` |

## 二、UI 控件操作（BasePage 方法）

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| 控件点击 | `self.click(control, timeout, move_duration, press_duration, move_steps)` | 点击 UI 控件 |
| 控件双击 | `self.double_click(control, timeout, interval)` | 双击 UI 控件 |
| 控件检查 | `self.find_control(control, timeout)` | 检查控件是否存在，找到返回 `True`，未找到返回 `False` |
| 控件输入 | `self.find_control_and_input(input_control, content, timeout, clear)` | 查找控件并输入内容，`clear=True` 先清空 |
| 控件滚动查找 | `self.find_control_by_scroll_up_and_down(control, max_scroll_down, max_scroll_up, scroll_interval, scroll_amount)` | 通过滚动查找控件，找到返回 `True`，未找到返回 `False` |
| 控件异常 | `control_raise(control, description, timeout)` | 控件必须存在，否则抛 `TargetControlNotFoundError` |
| 控件相对鼠标点击 | `self.find_control_and_click_relative_cursor(control, offset_x, offset_y, timeout, description)` | 查找控件后相对鼠标位置偏移点击 |

## 三、键盘/剪贴板操作（BasePage 方法）

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| 输入字符 | `self.send_contents(str_content)` | 输入字符 |
| 回车键 | `self.enter()` | 输入回车键 |
| 全选 | `self.selectAll()` | `{Ctrl}{A}` |
| 删除 | `self.delete()` | `{Delete}` |
| 复制 | `self.copy()` | `{Ctrl}{C}` |
| 粘贴 | `self.paste()` | `{Ctrl}{V}` |
| 输出剪贴板 | `self.clip_output()` | 输出剪贴板内容 |
| 发送按键 | `self.send_keys(keys, wait_time=0.5)` | 静态方法，发送键盘按键组合 |
| 直接点击坐标 | `self.click_coord(x, y, wait_time=0.5)` | 静态方法，直接点击坐标 |
| 移动到坐标 | `self.move_to(x, y, wait_time=0.5)` | 静态方法，移动鼠标到指定坐标 |
| 相对鼠标点击 | `self.click_mouse_relative_positon(offset_x=0, offset_y=0)` | 相对当前鼠标位置偏移点击 |

## 四、文件管理器操作（BasePage 方法）

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| 输入路径 | `self.input_file_path(file_path)` | 文件管理器输入路径 |
| 打开文件 | `self.open_file(filename)` | 打开文件/点击打开 |

## 五、等待操作（BasePage 方法）

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| 等待控件出现 | `self.wait_for_control_appear(control, timeout=600)` | 循环等待控件出现，出现返回 `True`，超时返回 `False` |
| 等待控件消失 | `self.wait_for_control_disappear(control, timeout=30)` | 循环等待控件消失，消失返回 `True`，超时返回 `False` |
| 等待图像出现 | `self.wait_for_image_appear(image_path, timeout=30)` | 循环等待图像出现，出现返回 `True`，超时返回 `False` |
| 等待图像消失 | `self.wait_for_image_disappear(image_path, timeout=10)` | 循环等待图像消失，消失返回 `True`，超时返回 `False` |

## 六、ScreenElement 方法（captureScreen.py）

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| 查找坐标 | `element.find(region=None, threshold=None, save_debug=None)` | 查找图像中心坐标，返回 `(x, y)` 或 `None` |
| 是否存在 | `element.exists(region=None, threshold=None, timeout=0)` | 超时等待判断，存在返回 `True`，不存在返回 `False` |
| 查找并点击 | `element.click(region=None, threshold=None, delay=None, timeout=0)` | 超时等待后点击，成功返回 `True`，失败返回 `False` |
| 移动到位置 | `element.move_to_position(region=None, threshold=None, delay=None, timeout=0)` | 超时等待后移动鼠标，成功返回 `True`，失败返回 `False` |
| 双击 | `element.double_click(region=None, threshold=None, delay=None, timeout=0)` | 超时等待后双击，成功返回 `True`，失败返回 `False` |
| 滚动查找 | `element.scroll_and_find(max_scroll_down=20, max_scroll_up=20)` | 先向下再向上滚动查找，找到返回 `True`，未找到返回 `False` |
| 相对偏移点击 | `element.click_relative_to_element(offset_x=0, offset_y=0, timeout=10.0)` | 相对图像中心偏移点击，超时抛 `TimeoutError` |

## 七、异常处理函数

| 函数 | 说明 |
|------|------|
| `control_raise(control, description, timeout=10)` | 验证控件必须存在，不存在抛 `TargetControlNotFoundError` |
| `element_raise(template_path, description, timeout=10, interval=0.5)` | 验证图片/图标必须存在，不存在抛 `TargetElementNotFoundError` |

> **导入方式**：`from commons.utils.targetNotFoundError import control_raise, element_raise`