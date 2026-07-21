# example_4: 测试用例分层（测试组件化）

## 概述

演示了如何使用 API 和 Suite 进行测试用例分层，实现测试组件化和复用。

## 文件结构

```
example_4/
├── example_4.py              # 测试执行入口
├── example_4.yaml            # 测试用例文件
├── DemoRunner.py             # 自定义 Runner 实现
└── dependencies/
    ├── api/
    │   └── test_api.yaml     # API 用例（可被重复引用）
    └── suite/
        └── test_suite.yaml   # Suite 用例（封装多个 case）
```

## 运行方式

```bash
cd example_4
python example_4.py
```

## 关键知识点

### API 用例

API 用例存放在 `dependencies/api/` 目录下，使用 `def` 定义函数入口：

```yaml
# dependencies/api/test_api.yaml
- api:
    def: add_api($arg1, $arg2, $exp)
    demotest: ${add($arg1, $arg2)}
    demoverify: ${_is($exp)}
```

### Suite 用例

Suite 用例存放在 `dependencies/suite/` 目录下，在 `project` 块中定义 `def`：

```yaml
# dependencies/suite/test_suite.yaml
- project:
    def: suite_test()

- case:
    name: suite 1
    api: add_api(1, 2, 3)
```

### 调用方式

在 case 中通过 `api` 或 `suite` 关键字调用：

```yaml
- case:
    name: case 0
    suite: suite_test()

- case:
    name: case 1
    api: add_api(1, 2, 100)
```

## 预期结果

执行后会生成包含 6 条测试用例的报告：
- suite 中的 3 条用例：全部通过
- case 中的 3 条用例：2 条失败（验证期望值不匹配），1 条通过

## 设计思路

- **API 用例**：封装单个测试步骤，参数化设计，便于重复调用
- **Suite 用例**：封装多个 API/case，形成稳定的测试场景
- **Case 用例**：编写异常测试场景或组合调用
