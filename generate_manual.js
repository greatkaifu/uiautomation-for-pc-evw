const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat,
        HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak, TabStopType, TabStopPosition,
        TableOfContents } = require('docx');
const fs = require('fs');

// 颜色定义
const C_PRIMARY = "1A5FB4";
const C_SECONDARY = "2ECC71";
const C_DARK = "2C3E50";
const C_GRAY = "666666";
const C_LIGHT_BG = "F5F5F5";
const C_TABLE_HEAD = "D5E8F0";
const C_CODE_BG = "F0F0F0";

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text, bold: true, size: 36, color: C_PRIMARY })]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 150 },
    children: [new TextRun({ text, bold: true, size: 28, color: C_PRIMARY })]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 24, color: C_DARK })]
  });
}

function p(text, opts = {}) {
  const { bold = false, color = C_DARK, size = 22 } = opts;
  return new Paragraph({
    spacing: { before: 60, after: 60, line: 360 },
    children: [new TextRun({ text, bold, size, color })]
  });
}

function code(text) {
  return new Paragraph({
    shading: { fill: C_CODE_BG, type: ShadingType.CLEAR },
    spacing: { before: 40, after: 40, line: 280 },
    indent: { left: 360 },
    children: [new TextRun({ text, font: "Consolas", size: 18, color: C_DARK })]
  });
}

function multiCode(lines) {
  return new Paragraph({
    shading: { fill: C_CODE_BG, type: ShadingType.CLEAR },
    spacing: { before: 60, after: 60, line: 280 },
    indent: { left: 360 },
    children: lines.map((line, i) => new TextRun({
      text: line + (i < lines.length - 1 ? "\n" : ""),
      font: "Consolas",
      size: 18,
      color: C_DARK,
      break: i < lines.length - 1 ? 1 : 0
    }))
  });
}

function note(text) {
  return new Paragraph({
    shading: { fill: "FFF3CD", type: ShadingType.CLEAR },
    spacing: { before: 80, after: 80, line: 320 },
    indent: { left: 360, right: 360 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 12, color: "FFC107", space: 8 }
    },
    children: [
      new TextRun({ text: "提示：", bold: true, size: 20, color: "856404" }),
      new TextRun({ text, size: 20, color: "856404" })
    ]
  });
}

function warning(text) {
  return new Paragraph({
    shading: { fill: "F8D7DA", type: ShadingType.CLEAR },
    spacing: { before: 80, after: 80, line: 320 },
    indent: { left: 360, right: 360 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 12, color: "DC3545", space: 8 }
    },
    children: [
      new TextRun({ text: "注意：", bold: true, size: 20, color: "721C24" }),
      new TextRun({ text, size: 20, color: "721C24" })
    ]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 40, after: 40, line: 360 },
    children: [new TextRun({ text, size: 22, color: C_DARK })]
  });
}

function numbered(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { before: 40, after: 40, line: 360 },
    children: [new TextRun({ text, size: 22, color: C_DARK })]
  });
}

function makeTable(headers, rows, colWidths) {
  const totalWidth = 9360;
  const cw = colWidths || headers.map(() => Math.floor(totalWidth / headers.length));
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: cw,
    rows: [
      new TableRow({
        children: headers.map(h => new TableCell({
          borders,
          width: { size: cw[headers.indexOf(h)], type: WidthType.DXA },
          shading: { fill: C_TABLE_HEAD, type: ShadingType.CLEAR },
          margins: { top: 60, bottom: 60, left: 100, right: 100 },
          children: [new Paragraph({
            children: [new TextRun({ text: h, bold: true, size: 20, color: C_DARK })]
          })]
        }))
      }),
      ...rows.map(row => new TableRow({
        children: row.map((cell, ci) => new TableCell({
          borders,
          width: { size: cw[ci], type: WidthType.DXA },
          margins: { top: 50, bottom: 50, left: 100, right: 100 },
          children: [new Paragraph({
            children: [new TextRun({ text: cell, size: 20, color: C_DARK })]
          })]
        }))
      }))
    ]
  });
}

// ========== 构建文档 ==========

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Microsoft YaHei", size: 22 }
      }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Microsoft YaHei", color: C_PRIMARY },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Microsoft YaHei", color: C_PRIMARY },
        paragraph: { spacing: { before: 300, after: 150 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Microsoft YaHei", color: C_DARK },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "EaseUS VoiceWave UI自动化测试框架使用手册", size: 16, color: C_GRAY, italics: true })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", size: 18, color: C_GRAY }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: C_GRAY }),
            new TextRun({ text: " 页", size: 18, color: C_GRAY })
          ]
        })]
      })
    },
    children: [
      // ====== 封面 ======
      new Paragraph({ spacing: { before: 2000 } }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "EaseUS VoiceWave", size: 56, bold: true, color: C_PRIMARY, font: "Microsoft YaHei" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "UI 自动化测试框架使用手册", size: 40, color: C_DARK, font: "Microsoft YaHei" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ text: "基于 Python + uiautomation + pytest + Allure", size: 24, color: C_GRAY, font: "Microsoft YaHei" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 1200 },
        children: [new TextRun({ text: "版本：v1.0", size: 22, color: C_GRAY })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "日期：2026-06-11", size: 22, color: C_GRAY })]
      }),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 目录 ======
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 400 },
        children: [new TextRun({ text: "目  录", size: 40, bold: true, color: C_PRIMARY })]
      }),
      new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" }),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第一章：项目概述 ======
      h1("第一章  项目概述"),

      h2("1.1 项目简介"),
      p("本项目是一个基于 pytest 的 PC 端 UI 自动化测试框架，用于测试 EaseUS VoiceWave 桌面应用程序。VoiceWave 是一款 Windows 平台的音频变声软件，提供实时变声、文件变声、音效板、社区、声音创建等功能。"),
      p("框架采用三层 POM（Page Object Model）架构设计，封装了 uiautomation 库的核心操作，支持控件定位和图像识别双模式元素查找，并集成 Allure 生成可视化测试报告。"),

      h2("1.2 技术栈"),
      makeTable(
        ["分类", "技术/工具", "版本", "用途"],
        [
          ["UI 自动化", "uiautomation", "2.0.29", "Windows UI 自动化核心库"],
          ["UI 自动化", "pyautogui", "0.9.54", "鼠标键盘模拟操作"],
          ["图像识别", "opencv-python", "4.12.0.88", "OpenCV 图像处理与模板匹配"],
          ["图像识别", "Pillow", "11.1.0", "图像处理辅助"],
          ["测试框架", "pytest", "9.0.2", "测试框架核心"],
          ["测试框架", "pytest-dependency", "0.6.1", "用例依赖管理"],
          ["测试报告", "allure-pytest", "2.14.0", "Allure 测试报告集成"],
          ["系统工具", "WMI", "1.5.1", "Windows 管理接口（网络控制等）"],
          ["系统工具", "psutil", "7.2.1", "进程管理"],
          ["其他", "selenium", "4.41.0", "浏览器自动化（辅助功能）"],
        ],
        [1800, 2400, 1600, 3560]
      ),

      h2("1.3 架构设计"),
      p("框架采用三层 POM 架构："),
      bullet("基础层（bases/）：封装 uiautomation 核心操作，提供 BasePage 基类、图像识别（captureScreen）、鼠标控制（mouseController）"),
      bullet("POM 层（pom/）：封装各页面业务逻辑，每个页面对应一个 Python 类"),
      bullet("测试层（testcase/）：编写 pytest 测试用例，调用 POM 层方法完成测试流程"),
      p("此外，commons/utils/ 目录提供了配置管理、日志、进程控制、语言切换等工具模块。"),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第二章：环境搭建 ======
      h1("第二章  环境搭建"),

      h2("2.1 系统要求"),
      bullet("操作系统：Windows 10/11（64位）"),
      bullet("Python 版本：3.8 及以上"),
      bullet("被测应用：EaseUS VoiceWave 已安装"),
      bullet("权限：管理员权限（部分操作如网络控制需要）"),

      h2("2.2 Python 环境配置"),
      p("建议使用虚拟环境："),
      code("python -m venv venv"),
      code("venv\\Scripts\\activate"),

      h2("2.3 安装依赖"),
      p("项目依赖已记录在 requirements.txt 中，执行以下命令安装："),
      code("pip install -r requirements.txt"),

      h2("2.4 配置文件"),
      p("config/config.ini 文件包含应用安装路径等关键配置，请确保路径正确："),
      code("[install]"),
      code("path = C:\\Program Files (x86)\\EaseUS\\VoiceWave\\bin\\easeus.voicewave.exe"),
      warning("请根据实际安装路径修改 config.ini 中的 path 配置，否则测试将无法启动被测应用。"),

      h2("2.5 Allure 命令行工具"),
      p("Allure 报告需要安装命令行工具，下载地址："),
      p("https://github.com/allure-framework/allure2/releases"),
      p("安装后确保 allure 命令已加入系统 PATH。"),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第三章：项目结构 ======
      h1("第三章  项目结构"),

      h2("3.1 目录结构"),
      code("python-uiautomation-for-pc-evw/"),
      code("├── bases/                      # 基础层"),
      code("│   ├── basePage.py            # BasePage 基类（核心封装）"),
      code("│   ├── captureScreen.py       # 图像识别与元素定位"),
      code("│   └── mouseController.py     # 平滑鼠标控制"),
      code("├── commons/"),
      code("│   └── utils/                 # 工具模块"),
      code("│       ├── configmanager.py   # INI 配置管理"),
      code("│       ├── myLogging.py       # 日志系统"),
      code("│       ├── killProcess.py     # 进程管理"),
      code("│       ├── languageSet.py     # 语言切换（注册表操作）"),
      code("│       ├── targetNotFoundError.py  # 异常封装"),
      code("│       └── ...                # 其他工具"),
      code("├── pom/                        # POM 页面对象层"),
      code("│   ├── voicewave_home_page.py            # 首页/实时变声"),
      code("│   ├── voicewave_file_voicechanger_page.py # 文件变声"),
      code("│   ├── voicewave_soundboard_page.py      # 音效板"),
      code("│   ├── voicewave_community_page.py       # 社区"),
      code("│   ├── voicewave_voice_creation_page.py  # 声音创建"),
      code("│   ├── voicewave_setting_page.py         # 设置"),
      code("│   ├── voicewave_login_page.py           # 登录"),
      code("│   └── ..."),
      code("├── testcase/                   # 测试用例层"),
      code("│   ├── test_nav4_file_voice_changer.py"),
      code("│   ├── test_nav5_voice_creation.py"),
      code("│   ├── test_language.py"),
      code("│   └── ..."),
      code("├── config/"),
      code("│   └── config.ini             # 配置文件"),
      code("├── conftest.py                # pytest fixtures"),
      code("├── pytest.ini                 # pytest 配置"),
      code("├── requirements.txt           # 依赖列表"),
      code("└── README.md                  # 项目说明"),

      h2("3.2 各模块职责"),
      makeTable(
        ["目录", "职责说明", "核心文件"],
        [
          ["bases/", "封装底层 UI 操作，提供统一的元素定位、点击、输入等方法", "basePage.py"],
          ["commons/utils/", "提供各类工具函数：配置读写、进程管理、语言切换、日志等", "configmanager.py, languageSet.py"],
          ["pom/", "封装各页面的业务逻辑，每个类对应一个功能页面", "voicewave_home_page.py 等"],
          ["testcase/", "编写测试用例，组织测试流程，调用 POM 层完成测试", "test_*.py"],
          ["config/", "存放配置文件，如应用安装路径", "config.ini"],
        ],
        [1600, 4800, 2960]
      ),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第四章：快速入门 ======
      h1("第四章  快速入门"),

      h2("4.1 编写第一个 POM 页面类"),
      p("所有页面类应继承 BasePage，通过 super().__init__(main_window) 初始化。"),
      code("# pom/example_page.py"),
      code("# -*- coding: utf-8 -*-"),
      code("from bases.basePage import BasePage"),
      code(""),
      code("class ExamplePage(BasePage):"),
      code("    def __init__(self, main_window):"),
      code("        super().__init__(main_window)"),
      code(""),
      code("    def click_some_button(self):"),
      code("        btn = self.main_window.ButtonControl(Name='Some Button')"),
      code("        self.click(btn)"),

      note("POM 类中应封装业务操作，而非暴露底层定位逻辑。测试用例只调用业务方法。"),

      h2("4.2 编写第一个测试用例"),
      p("测试文件以 test_ 开头，测试类以 Test 开头，测试方法以 test_ 开头。"),
      code("# testcase/test_example.py"),
      code("# -*- coding: utf-8 -*-"),
      code("import pytest"),
      code("import allure"),
      code("from pom.example_page import ExamplePage"),
      code(""),
      code("class TestExample:"),
      code("    @pytest.mark.test"),
      code("    @allure.story('示例功能')"),
      code("    @allure.title('点击某个按钮')"),
      code("    def test_click_button(self, active_window):"),
      code("        page = ExamplePage(active_window)"),
      code("        page.click_some_button()"),

      h2("4.3 运行测试"),
      p("在项目根目录执行 pytest 命令："),
      code("# 运行所有标记为 test 的用例"),
      code("pytest -v -s -m test"),
      code(""),
      code("# 运行指定文件"),
      code("pytest testcase/test_example.py -v"),
      code(""),
      code("# 运行指定类中的指定方法"),
      code("pytest testcase/test_example.py::TestExample::test_click_button -v"),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第五章：核心 API 使用指南 ======
      h1("第五章  核心 API 使用指南"),

      h2("5.1 控件定位"),
      p("框架支持通过 uiautomation 的控件链进行元素定位："),
      code("# 链式定位控件"),
      code("control = main_window.GroupControl(Name='Panel').ButtonControl(Name='OK')"),

      h3("5.1.1 控件点击"),
      code("self.click(control, timeout=10, move_duration=0.8, press_duration=0.3, move_steps=45)"),
      bullet("timeout：等待控件出现的超时时间（秒）"),
      bullet("move_duration：鼠标移动到控件的时长（秒）"),
      bullet("press_duration：鼠标按下后保持的时长（秒）"),
      bullet("move_steps：移动分步数，值越大轨迹越平滑"),

      h3("5.1.2 控件双击"),
      code("self.double_click(control, timeout=10, interval=0.1)"),

      h3("5.1.3 控件查找"),
      code("# 查找控件是否存在"),
      code("found = self.find_control(control, timeout=10)"),
      code("# 返回 True 或 None"),

      h3("5.1.4 控件滚动查找"),
      code("found = self.find_control_by_scroll_up_and_down("),
      code("    control,"),
      code("    max_scroll_down=20,"),
      code("    max_scroll_up=20,"),
      code("    scroll_interval=0.5,"),
      code("    scroll_amount=1"),
      code(")"),

      h2("5.2 图像识别"),
      p("当控件定位困难时，可以使用图像识别定位元素。"),

      h3("5.2.1 图像点击"),
      code("self.find_element_and_click('nav1_home/play_button.png', timeout=10)"),

      h3("5.2.2 图像查找"),
      code("exists = self.find_element('nav1_home/play_button.png', timeout=10)"),

      h3("5.2.3 相对图像点击"),
      code("self.click_relative_to_element('nav1_home/icon.png', offset_x=100, offset_y=50)"),

      h3("5.2.4 图像滚动查找"),
      code("found = self.find_element_by_scroll_up_and_down("),
      code("    'nav1_home/target.png',"),
      code("    max_scroll_down=20,"),
      code("    max_scroll_up=20"),
      code(")"),

      note("图像模板应存放在 resources/images/ 目录下，路径参数使用相对路径（不含 resources/images/ 前缀）。"),

      h2("5.3 输入操作"),

      h3("5.3.1 控件输入"),
      code("self.find_control_and_input(input_control, 'Hello World', timeout=10, clear=True)"),

      h3("5.3.2 图像位置输入"),
      code("self.find_element_and_input('nav1_home/input.png', 'Hello World', timeout=10)"),

      h3("5.3.3 键盘操作"),
      code("self.send_keys('{Ctrl}{A}')   # 全选"),
      code("self.send_keys('{Delete}')    # 删除"),
      code("self.send_keys('{Enter}')     # 回车"),
      code("self.send_keys('{Ctrl}{C}')   # 复制"),
      code("self.send_keys('{Ctrl}{V}')   # 粘贴"),

      h2("5.4 文件管理器操作"),
      p("框架封装了文件管理器的常用操作："),

      h3("5.4.1 输入文件路径"),
      code("self.input_file_path(r'C:\\Users\\admin\\Desktop\\test_audio.mp3')"),

      h3("5.4.2 打开文件"),
      code("self.open_file('test_audio.mp3')"),

      h2("5.5 异常处理"),
      p("框架提供了统一的异常处理策略："),

      h3("5.5.1 图像元素异常"),
      code("from commons.utils.targetNotFoundError import element_raise"),
      code("element_raise('nav1_home/icon.png', '首页播放按钮', timeout=10)"),
      p("当图像元素未找到时，抛出 TargetElementNotFoundError，附带清晰的中文描述。"),

      h3("5.5.2 UI 控件异常"),
      code("from commons.utils.targetNotFoundError import control_raise"),
      code("control = main_window.ButtonControl(Name='OK')"),
      code("control_raise(control, '确认按钮', timeout=10)"),
      p("当 UI 控件未找到时，抛出 TargetControlNotFoundError。"),

      warning("统一使用 element_raise 处理图像/图标异常，使用 control_raise 处理 UI 控件异常，确保测试失败信息清晰可读。"),

      h2("5.6 等待方法"),
      makeTable(
        ["方法", "参数", "说明"],
        [
          ["wait_for_image_appear", "image_path, timeout=30", "等待图像出现"],
          ["wait_for_image_disappear", "image_path, timeout=10", "等待图像消失"],
          ["wait_for_control_appear", "control, timeout=600", "等待控件出现"],
          ["wait_for_control_disappear", "control, timeout=30", "等待控件消失"],
        ],
        [2800, 3800, 2760]
      ),

      h2("5.7 Allure 截图"),
      code("self.allure_screenshot(name='操作后截图')"),
      p("截取当前屏幕并附加到 Allure 报告中，用于问题定位。"),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第六章：Fixture 使用指南 ======
      h1("第六章  Fixture 使用指南"),

      h2("6.1 内置 Fixture 列表"),
      makeTable(
        ["Fixture 名称", "作用域", "用途", "环境配置"],
        [
          ["active_window", "module", "已激活用户环境", "SHOW_EXIT_WINDOW=false"],
          ["newuser_language_window", "function", "未激活新用户 + 语言切换", "delete_voice_wave_ini()"],
          ["olduser_language_window", "function", "未激活老用户 + 语言切换", "modify_time() + delete_start_time()"],
          ["creation_language_window", "function", "声音创建多语言环境", "6种语言参数化"],
          ["login_window", "function", "登录测试环境", "delete_voice_wave_ini()"],
          ["active_window_function", "function", "已激活用户（含清理）", "完整前后置"],
          ["window", "module", "标准窗口（含清理）", "delete_voice_wave_ini()"],
          ["main_window", "class", "新用户完整环境", "含弹窗关闭 + 进程清理"],
          ["old_main_window", "function", "老用户完整环境", "modify_time()"],
          ["Inactive_main_window", "function", "未激活环境", "清除激活文件"],
        ],
        [2200, 1200, 2800, 3160]
      ),

      h2("6.2 Fixture 作用域说明"),
      p("pytest 的 fixture 支持以下作用域："),
      bullet("session：整个测试会话只执行一次"),
      bullet("module：每个测试模块文件执行一次"),
      bullet("class：每个测试类执行一次"),
      bullet("function：每个测试方法执行一次（默认）"),

      h2("6.3 使用 Fixture"),
      p("在测试方法中，将 fixture 名称作为参数传入即可："),
      code("def test_example(self, active_window):"),
      code("    # active_window 是 fixture 返回的主窗口对象"),
      code("    page = HomePage(active_window)"),

      h2("6.4 自定义 Fixture"),
      p("在 conftest.py 中定义，可被同目录及子目录下的测试文件使用："),
      code("import pytest"),
      code(""),
      code("@pytest.fixture(scope='function')"),
      code("def my_custom_fixture():"),
      code("    # 前置操作"),
      code("    yield 'some_data'"),
      code("    # 后置清理操作"),

      note("yield 之前的代码为前置操作，yield 返回数据给测试用例，yield 之后的代码为后置清理操作。"),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第七章：测试执行与报告 ======
      h1("第七章  测试执行与报告"),

      h2("7.1 运行测试"),
      makeTable(
        ["命令", "说明"],
        [
          ["pytest -v -s -m test", "运行所有标记为 @pytest.mark.test 的用例"],
          ["pytest -m 'ui' -v", "运行标记为 ui 的用例"],
          ["pytest -m 'smoke' -v", "运行冒烟测试"],
          ["pytest testcase/test_example.py -v", "运行指定测试文件"],
          ["pytest -k 'keyword' -v", "按关键字匹配运行用例"],
          ["pytest -x -v", "遇到第一个失败即停止"],
          ["pytest --lf -v", "只运行上次失败的用例"],
        ],
        [4200, 5160]
      ),

      h2("7.2 生成 Allure 报告"),
      p("分两步生成 Allure 可视化报告："),

      h3("步骤 1：生成报告数据"),
      code("pytest testcase/ --alluredir=allure-results --clean-alluredir -v"),
      p("此命令会清空历史结果，执行测试并将结果写入 allure-results 目录。"),

      h3("步骤 2：生成 HTML 报告"),
      code("allure generate -o report -c allure-results/"),
      p("生成可视化的 HTML 报告到 report 目录。"),

      h3("步骤 3：查看报告"),
      code("allure open report/"),
      p("自动在浏览器中打开报告。"),

      h2("7.3 报告效果"),
      p("Allure 报告提供以下信息："),
      bullet("测试用例执行结果统计（通过/失败/跳过）"),
      bullet("每个用例的详细步骤和耗时"),
      bullet("截图附件（通过 allure_screenshot 附加）"),
      bullet("历史趋势分析"),
      bullet("测试套件分类展示"),

      // 分页
      new Paragraph({ children: [new PageBreak()] }),

      // ====== 第八章：最佳实践 ======
      h1("第八章  最佳实践"),

      h2("8.1 编码规范"),
      numbered("文件编码：所有 Python 文件头部添加 # -*- coding: utf-8 -*-"),
      numbered("文件命名：POM 类使用 voicewave_xxx_page.py，测试文件使用 test_xxx.py"),
      numbered("类命名：POM 类使用 XxxPage，测试类使用 TestXxx"),
      numbered("方法命名：业务方法使用动词开头（如 click_xxx, input_xxx）"),
      numbered("测试方法：使用 test_ 前缀，描述测试场景"),

      h2("8.2 元素定位策略"),
      bullet("优先使用控件链定位（如 main_window.ButtonControl(Name='OK')）"),
      bullet("控件链无法定位时，使用图像识别作为兜底方案"),
      bullet("避免使用 time.sleep()，改用 auto.WaitForExist() 或框架封装的等待方法"),
      bullet("定位控件时尽量使用 Name 和 ClassName 组合，提高稳定性"),

      h2("8.3 异常处理策略"),
      bullet("图像/图标定位失败：使用 element_raise() 抛出 TargetElementNotFoundError"),
      bullet("UI 控件定位失败：使用 control_raise() 抛出 TargetControlNotFoundError"),
      bullet("不要在测试用例中直接处理异常，让异常抛出以便 Allure 记录失败原因"),

      h2("8.4 调试技巧"),
      bullet("使用 pytest -s 参数查看 print 输出和日志"),
      bullet("使用 pytest --pdb 在失败时进入调试模式"),
      bullet("在关键步骤后添加 self.allure_screenshot() 记录屏幕状态"),
      bullet("查看 logs/UI_rotating.txt 获取详细日志信息"),

      h2("8.5 常见问题"),

      h3("Q1：主窗口未找到，测试退出"),
      p("A：检查 config.ini 中的应用路径是否正确，确认应用能否正常启动。"),

      h3("Q2：图像识别找不到元素"),
      p("A：检查图像模板分辨率是否与当前屏幕一致；不同 DPI 缩放比例可能导致匹配失败。"),

      h3("Q3：Allure 报告生成失败"),
      p("A：确认已安装 Allure 命令行工具并已加入 PATH；尝试先删除 allure-results 目录再重新生成。"),

      h3("Q4：测试运行后进程未清理"),
      p("A：检查 fixture 的后置清理代码是否正常执行；手动运行 kill_process_by_name('easeus.voicewave.exe') 清理。"),

      h2("8.6 性能优化建议"),
      bullet("合理设置 timeout，避免过长的等待时间"),
      bullet("使用 module 或 class 作用域的 fixture 减少重复启动应用的开销"),
      bullet("图像模板尽量压缩到必要大小，减少 OpenCV 匹配耗时"),
      bullet("批量运行测试时，关闭不必要的日志输出以提高速度"),

      // 结束
      new Paragraph({ spacing: { before: 800 } }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "—  完  —", size: 24, color: C_GRAY })]
      }),
    ]
  }]
});

const outputPath = "G:\\project\\python-uiautomation-for-pc-evw\\EaseUS_VoiceWave_UI自动化测试框架_使用手册.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("Word 文档已生成: " + outputPath);
}).catch(err => {
  console.error("生成失败:", err);
});
