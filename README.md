# rtsf

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

**rtsf** (Rock4 Test Service Framework) is a lightweight, extensible test automation framework that provides keyword-driven and data-driven testing capabilities. It serves as a foundation for building various automation testing frameworks for HTTP APIs, web applications, mobile apps, and desktop clients.

> **English**: rtsf is a lightweight test automation framework designed to provide keyword-driven and data-driven testing capabilities. It supports test case layering (case/api/suite), data-driven testing with CSV files, and extensible runner customization.

> **中文**: rtsf 是一个轻量级的测试自动化框架，提供关键字驱动和数据驱动的测试能力。支持测试用例分层（case/api/suite）、CSV数据驱动测试以及可扩展的自定义Runner。

## 特性 / Features

- **关键字驱动测试**：支持自定义关键字绑定
- **数据驱动测试**：CSV文件参数化，支持随机/顺序读取，自动执行笛卡儿积
- **测试用例分层**：支持 case、api、suite 三种用例类型，实现测试组件化
- **可扩展架构**：通过重写 Runner 轻松扩展执行逻辑
- **HTML测试报告**：自动生成可视化测试报告
- **日志追踪**：完整的测试执行日志记录
- **命令行友好**：方便接入持续集成系统

## 目录 / Table of Contents

- [安装](#安装)
- [快速入门](#快速入门)
- [测试用例介绍](#测试用例介绍)
- [数据驱动](#数据驱动)
- [自定义Runner](#自定义runner)
- [测试用例分层](#测试用例分层)
- [项目结构](#项目结构)
- [生态系统](#生态系统)
- [贡献](#贡献)
- [许可证](#许可证)

## 安装

```bash
pip install rtsf
```

## 快速入门

```python
from rtsf.p_executer import TestRunner, Runner

runner = TestRunner(runner=Runner).run('test.yaml')
runner.gen_html_report()
```

## 测试用例介绍

rtsf 支持三种用例类型：`case`、`api`、`suite`，支持测试用例分层和组件化。

### Case 用例

```yaml
# test.yaml
- project:
    name: demo project
    module: test baidu

- case:
    name: case 1

- case:
    name: case call api
    api: test_api()
```

### API 用例

API 用例可被其他用例重复引用，存放在 `dependencies/api/` 目录下。

```yaml
# dependencies/api/test_api.yaml
- api:
    def: test_api($arg1, $arg2)
```

### Suite 用例

Suite 用例封装多个 case，存放在 `dependencies/suite/` 目录下。

```yaml
# dependencies/suite/test_suite.yaml
- project:
    def: test_suite($arg1, $arg2)

- case:
    name: suite case 1
```

### 变量和函数引用

- 引用函数：`${function_name(args)}`
- 引用变量：`$variable_name`

## 数据驱动

在 `project` 块中添加 `data` 关键字，支持 CSV 文件参数化。

```yaml
- project:
    name: demo project
    data:
        - csv: devices.csv
          by: Random
        - csv: username_password.csv

- case:
    name: test-$username-$devices
```

CSV 文件格式：
```csv
username,password
user1,pass1
user2,pass2
```

- `by`: 读取方式，`Random`（随机）或 `Sequential`（顺序，默认）
- 多个 CSV 会自动执行笛卡儿积

## 自定义 Runner

通过重写 `Runner.run_test` 方法扩展执行逻辑：

```python
from rtsf.p_executer import Runner

class DemoRunner(Runner):
    def run_test(self, testcase_dict, variables, driver_map):
        fn, driver = driver_map
        fn_logger = self.tracers[fn]
        parser = self.parser
        
        parser.bind_functions({"add": lambda x, y: x + y})
        parser.update_binded_variables(variables)
        
        fn_logger.start(self.proj_info["module"], testcase_dict["name"])
        
        try:
            fn_logger.step("execute test")
            fn_logger.ok("test passed")
        except Exception as e:
            fn_logger.error(e)
        
        fn_logger.stop()
```

完整示例代码参见 [examples/example_3](examples/example_3)。

## 测试用例分层

API 和 Suite 用例可以被重复引用，实现测试组件化：

```yaml
# dependencies/api/test_api.yaml
- api:
    def: add_api($arg1, $arg2, $exp)
    demotest: ${add($arg1, $arg2)}
    demoverify: ${_is($exp)}

# example.yaml
- case:
    name: use api
    api: add_api(1, 2, 3)
```

完整示例代码参见 [examples/example_4](examples/example_4)。

## 项目结构

```
rtsf/
├── __init__.py
├── __about__.py
├── p_applog.py          # 日志模块
├── p_compat.py          # 兼容性模块
├── p_exception.py       # 异常定义
├── p_executer.py        # 测试执行器
├── p_report.py          # HTML报告生成
├── p_testcase.py        # 测试用例解析
├── p_tracer.py          # 测试追踪器
├── p_common.py          # 向后兼容导出层
├── utils/               # 工具模块（拆分自p_common）
│   ├── __init__.py
│   ├── common_utils.py  # 通用工具（含map_function等）
│   ├── date_utils.py    # 日期工具
│   ├── file_utils.py    # 文件操作（YAML/JSON/CSV读取）
│   ├── fs_utils.py      # 文件系统工具（目录/文件操作）
│   ├── module_utils.py  # 模块工具（动态导入/配置搜索）
│   ├── progress_utils.py # 进度条工具
│   ├── setup_utils.py   # 安装工具
│   ├── wait_utils.py    # 等待工具（命令等待/连接检测）
│   └── zip_utils.py     # 压缩工具
└── tests/               # 单元测试
    ├── test_p_applog.py
    ├── test_p_common.py
    ├── test_p_executer.py
    ├── test_p_report.py
    ├── test_p_testcase.py
    └── test_p_tracer.py
```

## 项目背景

rtsf 的初衷是参考 [rock4automation](https://github.com/RockFeng0/rock4automation) 和 [httprunner](https://github.com/httprunner/httprunner) 项目，精简出一个轻量级的测试框架：

- **仅提供核心能力**：关键字驱动和数据驱动的程序框架
- **可扩展服务框架**：支持接入 Selenium、Appium、Requests 等技术形成业务框架
- **命令行友好**：方便接入持续集成系统
- **轻量设计**：少造轮子，多复用标准库和优秀开源项目

## 生态系统

![rtsf架构](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf/rtsf架构.png)

基于 rtsf 已构建的测试框架：

- **rtsf-http**：HTTP 接口测试框架 [GitHub](https://github.com/RockFeng0/rtsf-http)
- **rtsf-web**：Web 浏览器测试框架 [GitHub](https://github.com/RockFeng0/rtsf-web)
- **rtsf-app**：Android 移动端测试框架 [GitHub](https://github.com/RockFeng0/rtsf-app)
- **rtsf-win**：Windows 桌面客户端测试框架 [GitHub](https://github.com/RockFeng0/rtsf-win)

其他可接入方案：
- 计算机视觉：OpenCV
- 图像识别：Tesseract
- 像素对比：ImageDiff
- 游戏控件：pocoui

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
