# example_3: 自定义 Runner

## 概述

演示了如何通过重写 `Runner.run_test` 方法扩展执行逻辑，实现自定义的测试关键字绑定和验证。

## 文件结构

```
example_3/
├── example_3.py      # 测试执行入口
├── example_3.yaml    # 测试用例文件（包含自定义关键字）
└── DemoRunner.py     # 自定义 Runner 实现
```

## 运行方式

```bash
cd example_3
python example_3.py
```

## 关键知识点

### 重写 run_test 方法

```python
class DemoRunner(Runner):
    def run_test(self, testcase_dict, variables, driver_map):
        # testcase_dict: 单条测试用例
        # variables: 数据驱动变量（默认为 {}）
        # driver_map: 分布式驱动标识（默认为 ("", None)）
        ...
```

### 关键字绑定

通过 `parser.bind_functions()` 将 YAML 中的函数名映射到 Python 函数：

```python
yaml_keys = {"add": test_add, "mod": test_mod, '_is': verify_is}
parser.bind_functions(yaml_keys)
```

### 日志和报告记录

使用 `fn_logger`（Tracer 实例）记录测试过程：

- `start()` / `stop()`：开始/结束测试记录
- `step()` / `normal()`：记录步骤信息
- `ok()` / `fail()`：记录测试结果
- `error()`：记录异常信息

## 预期结果

执行后会生成包含 3 条测试用例的报告：
- demo test：通过（add(1,2)=3，验证_is(3)）
- demo test2：失败（mod(1,2)=1，验证_is(3)不通过）
- demo test3：错误（mod(1,0) 抛出除零异常）
