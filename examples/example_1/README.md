# example_1: 基础测试用例

## 概述

这是一个最基础的测试用例示例，演示了如何使用 rtsf 执行简单的 YAML 测试用例并生成 HTML 报告。

## 文件结构

```
example_1/
├── example_1.py    # 测试执行入口
└── example_1.yaml  # 测试用例文件
```

## 运行方式

```bash
cd example_1
python example_1.py
```

## 关键知识点

1. **TestRunner**：测试执行器，负责加载和运行测试用例
2. **run()**：运行指定的 YAML 测试用例文件
3. **gen_html_report()**：生成 HTML 测试报告

## 测试用例结构

```yaml
- project:
    name: demo project    # 项目名称
    module: test baidu    # 测试模块名称

- case:    
    name: www.baidu.com   # 用例名称
```

## 预期结果

执行后会在当前目录生成 HTML 测试报告，包含一条通过的测试用例。
