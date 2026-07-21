# example_2: 数据驱动测试

## 概述

演示了如何使用 CSV 文件进行数据驱动测试，支持随机/顺序读取，自动执行笛卡儿积。

## 文件结构

```
example_2/
├── example_2.py          # 测试执行入口
├── example_2.yaml        # 测试用例文件
├── devices.csv           # 设备数据
└── username_password.csv # 用户凭据数据
```

## 运行方式

```bash
cd example_2
python example_2.py
```

## 关键知识点

### 数据驱动配置

在 `project` 块中添加 `data` 关键字：

```yaml
data:
    - csv: devices.csv
      by: Random         # 随机读取
    - csv: username_password.csv  # 默认顺序读取
```

### CSV 文件格式

第一行定义变量名，后续行定义数据：

```csv
username,password
15312341230,1234567890
15312341231,1234567891
```

### 笛卡儿积

多个 CSV 会自动执行笛卡儿积，本示例会生成 2 × 3 = 6 条测试用例。

## 预期结果

执行后会生成包含 6 条测试用例的 HTML 报告。
