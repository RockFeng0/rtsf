# 项目初衷

> 为什么已经有了**[rock4automation](https://github.com/RockFeng0/rock4automation)痛点**的自动化测试框架的项目，还要另起一个rtsf项目，并且rtsf中使用的技术，rock4automation项目中已经涵盖？

因为，它存在的痛点很明显：

- rock4automation项目的初衷，是为了能快速重拾技术，是技术的合集，包含了新旧测试的技术。里边一些模块，是冗余的存在，这让项目本身很臃肿。如整合的一些自动化框架，selenium、appium、autoitv3、Microsoft UI Automation等等，关于性能的测试，整合了locust的一些用法。
- rock4automation项目,打包发布的程序，会将源码封装了exe或者加密为pyd，也就是说，发布出来的程序，不是一个源码，而是一个客户端程序，这就有违我开源的意图了
- rock4automation项目,打包了相关工具，比如appium-server，java.exe 等等，大量冗余的非项目源码的工具 

而rtsf(rock4 test service framework)项目的初衷：

- 参考rock4automation和httprunner的项目，我希望能精简一下rtsf，使它**仅仅提供一个测试的关键字驱动和数据驱动的程序框架**。
- 其次，我希望**rtsf是个可扩展的服务框架**，一些自动化技术的框架，可以依托rtsf，迅速形成一个有效的自动化测试相关的业务框架。如整合selenium形成web应用业务的自动化测试框架；整合requests等技术，形成http(s)接口层业务的自动化测试框架等。
- 另外，关于持续继承方面，我希望**rtsf是个命令行的工具**，依托它产生的自动化测试框架，可以接入持续集成的系统。
- 最后，我希望，依托rtsf产生的自动化测试项目，能够轻量，少造轮子，多复用标准库和优秀开源项目，

# 介绍


## rtsf-测试用例模型

> 测试用例模型，计划扩展为, yaml, xml, excel三种，目前已扩展的只有yaml测试用例模型 


### 测试用例基本结构
用例模型，基本保持[rock4automation项目](https://github.com/RockFeng0/rock4automation)的case模型

rtsf约定了基本结构，使用rtsf的时候，您**可以扩展约定字段**。基本结构，如下：

```
- project:
    name:
    module:
    data:
- case:
    name:
    responsible:
    tester:
    pre_command:
    steps:
    post_command:
    verify:
- case:    
    name:
    steps:
...
```

> 执行顺序  pre_command(List) -> steps(List) -> post_command(List) -> verify(List)

**preject定义测试集信息**

| project字段               | 描述                                        | 类型              |
| ------------- |:-------------:| -----:|
| name          | 项目名称或待测系统名称(必填)| 字符串       |
| module        | 测试集或功能模块名称(必填) | 字符串       |
| data          | 数据驱动，引用的数据(选填) | 列表      |

**case定义测试用例**

| case字段               | 描述                                        | 类型              |
| ------------- |:-------------:| -----:|
| name          | 描述 用例 (必填)，唯一性(必填) | 字符串       |
| responsible   | 用例责任人或者编写人(选填) | 字典           |
| tester        | 用例执行者或者测试人(选填) | 字典           |
| pre_command   | 测试的前置步骤或钩子(选填) | 列表           |
| steps         | 测试步骤 (必填)         | 列表           |
| post_command  | 测试的后置步骤或钩子(选填) | 列表           |
| verify        | 校验  (选填)           | 列表           |

**非约定字段，指程序框架不识别，用于记录和备注等作用**

| 常见非约定字段                 | 描述                                        | 类型              |
| ------------- |:-------------:| -----:|
| id            | 测试用例ID | 字符串       |
| desc          | 描述 用例   | 字符串       |


### 函数及变量替换的格式

变量和函数的替换，参照了httprunner项目的格式   该格式取代了我的[rock4automation项目](https://github.com/RockFeng0/rock4automation)中的， #var# 等替换规则

- 引用函数:   ${function_str}
- 引用变量:   $variable_str
- function_str 为字母、数字、下划线、横线、点号、等号、逗号组成的函数. 示例:  /api/${add(1, 2)}?_t=${get_timestamp()}   正则表示为: [a-zA-Z0-9.-_=,]
- function_str若含有特殊字符，将不会被识别， 解决方法是，使用全局变量.   示例,如:  a='@#$%^&'; $print($a)
- variable_str 为字母、数字、下划线组成的变量名.  正则表示为:  [a-zA-Z0-9_]  

**测试用例模型示例**

```
# yaml基本测试模型
# 分层用例，示例:
- project:
    name: xxx系统
    module: 分层用例-api-suite
    
- case:    
    # name 必填    ->测试用例名称,需确保唯一性. 调用api时，如果api定义了name，取api中name，否则，取case中name
    name: /api_name
    
    # 用例分层-使用 api时，必填
    api: test_api()

- case:    
    # name 必填    ->测试用例名称,需确保唯一性. 调用suite时，name取suite中的name
    name: /suite_name
    
    # 用例分层-使用 suite时，必填
    suite: test_suite()
    
- case:
    # id  desc 选填，非约定字段
    id: ATP-3
    desc: testset测试用例-模板（全字段）
    
    # name 必填    ->测试用例名称,需确保唯一性
    name: /baidu_test3
    
    # responsible 选填
    responsible: 罗科峰
    
    # tester 选填
    tester: 罗科峰
    
    # pre_command 选填
    pre_command:
        - Set(passwd = "123456")
    
    # steps 必填
    steps:
        # request 测试api或者 http /https 时使用
        - request:
            url: https://www.baidu.com
            method: GET
            headers:
            data:
        
        # webdriver 测试web ui 时使用
        - webdriver:
            by: css
            value: "#username"
            index: 0
            timeout: 10
            action: ${sendkey($username)}
        - webdriver:
            action: ${refresh}
        
        # mobiledriver 测试android UI 时使用
        - mobiledriver:
            action: ${refresh}
        
        # wpfdriver 测试pc wpf技术的客户端 ui 时使用    
        - wpfdriver:
            action: 
        
        # mfcdriver 测试pc mfc技术的客户端 ui 时使用    
        - mfcdriver:
            actiion:
    
    # post_command 选填
    post_command:
        - Set(passwd = "123456")
    
    # verify 选填
    verify:
        - VerifyCode("200")
```

## rtsf-数据驱动

数据驱动，其实很简单，在yaml的测试用例中，在project块，添加data关键字。

data关键字，以列表形式存在，每个列表项是一个字典，由两个key组成(csv, by)。跟loadrunner中参数化数据一样，csv第一行定义变量，第二行及以下行定义数据驱动的变量值
- csv后面接文件名称，该文件以csv形式存在于case同一路径。
- by是指读取csv格式的顺序， Random or Sequential。默认是Sequential，顺序读取。 该参数，可选填
- 笛卡儿积算法，会对多个data参数进行排列，rtsf会对排列的最终结果遍历执行当前测试集合

```
# 数据驱动，示例 data_driver.yaml
- project:
    name: xxx项目
    module: xxx项目-首页功能
    data:
        - csv: devices.csv
          by: Random      
        - csv: username_password.csv
        
- case:
    name: /baidu_test_$username-$password-$devices
    steps:
        - request:
            url: https://www.baidu.com
            method: GET
    verify:
        - ${VerifyCode(200)}
```

case路径下面，csv文件如下， 笛卡儿积计算的结果，是6条数据，会对case进行6次执行，每次执行会带入相应变量。 相应的报告，总共执行6条用例

```
# username_password.csv
username,password
15312341230,1234567890
15312341231,1234567891

# devices.csv
devices
android-0
android-1
android-2

```



## rtsf-测试用例分层(测试组件化)

- rtsf支持测试用例分层，允许测试用例的组件化
- 测试用例编写过程中，使用api关键字封装当前单个case，允许其他case进行调用,类似调用单个api一样
- 测试用例编写过程中，使用suite关键字，封装当前多个cases，允许其他case进行调用， 类似调用组件化模块一样
- api用例的原理: 合并。 是指测试用例调用api的时候，实际 合并 api用例的键值对。 **因此，如果case与api重复定义键值对，取api中键值对值** 
- suite用例的原理: 扩展。 是指测试用例调用suite的时候，实际是当前case替换并扩展为suite中的用例。 **所以，如果case与suite重复定义键值对，取suite中键值对值**

> 注意: 其内在逻辑，其实是，先加载api和suite,以dict形式存储在内置变量中，然后，加载测试集的用例，如果测试用例使用了api则合并，如果测试用例使用了suite则扩展。

分层用例的示例，参见[rtsf-http项目的介绍](https://github.com/RockFeng0/rtsf-http)

### api用例介绍

- api测试用例，实际上是一个最小单元的测试，封装后，便于被suite和testset重复引入
- api测试用例中的def的解析，参照了httprunner项目
- 存放路径, 测试用例同级目录下:  dependencies/api/*。yaml, dependencies/api/*。yml, dependencies/api/*。json

```
# api测试用例的示例：
- api:
    # def 必填
    def: test_api()    
    
    # id  desc 选填，非约定字段
    id: ATP-1
    desc: api测试用例-模板（字段与testset测试用例相同）
    
    # name 选填
    name: baidu_test1
    
    # pre_command 选填
    pre_command:
        - Set(passwd = "123456")
    
    # steps 必填
    steps:
        # request 测试api或者 http /https 时使用
        - request:
            url: https://www.baidu.com
            method: GET
            headers:
            data:
        
        # webdriver 测试web ui 时使用
        - webdriver:
            by: css
            value: "#username"
            index: 0
            timeout: 10
            action: ${sendkey($username)}
        - webdriver:
            action: ${refresh}
        
        # mobiledriver 测试android UI 时使用
        - mobiledriver:
            action: ${refresh}
        
        # wpfdriver 测试pc wpf技术的客户端 ui 时使用    
        - wpfdriver:
            action: 
        
        # mfcdriver 测试pc mfc技术的客户端 ui 时使用    
        - mfcdriver:
            actiion:
    
    # post_command 选填
    post_command:
        - Set(passwd = "123456")
    
    # verify 选填
    verify:
        - VerifyCode("200")
```


### suite用例介绍

- suite测试用例，实际上是，由一些api或者一些case，封装后的，相对稳定的，测试用例
- suite可以被testset引入
- 存放路径, 测试用例同级目录下:  dependencies/suite/*。yaml, dependencies/suite/*。yml, dependencies/suite/*。json

> suite的用例跟 testset差别不大，主要的是，在project中，添加def关键字，定义引入suite的函数入口

```
# suite测试套件的示例：
- project:
    def: test_suite()
            
- case:    
    # id  desc 选填，非约定字段
    id: ATP-2
    desc: suite测试用例-模板（字段与testset测试用例相同）
    
    # name 必填    ->测试用例名称,需确保唯一性
    name: /baidu_test2
    
    # responsible 选填
    responsible: 罗科峰
    
    # tester 选填
    tester: 罗科峰
    
    # pre_command 选填
    pre_command:
        - Set(passwd = "123456")
    
    # steps 必填
    steps:
        # request 测试api或者 http /https 时使用
        - request:
            url: https://www.baidu.com
            method: GET
            headers:
            data:
        
        # webdriver 测试web ui 时使用
        - webdriver:
            by: css
            value: "#username"
            index: 0
            timeout: 10
            action: ${sendkey($username)}
        - webdriver:
            action: ${refresh}
        
        # mobiledriver 测试android UI 时使用
        - mobiledriver:
            action: ${refresh}
        
        # wpfdriver 测试pc wpf技术的客户端 ui 时使用    
        - wpfdriver:
            action: 
        
        # mfcdriver 测试pc mfc技术的客户端 ui 时使用    
        - mfcdriver:
            actiion:
    
    # post_command 选填
    post_command:
        - Set(passwd = "123456")
    
    # verify 选填
    verify:
        - VerifyCode("200")
        
```

## rtsf-使用方法

- rtsf提供入口，允许自定义执行模块的扩展，这个过程有点类似python中重写threading.Thread类.
- 不同的是，rtsf需要重写rtsf.p_executer.Runner.run_test方法

### Runner.run_test重写
自定义case运行过程，就是重写 Runner.run_test的过程，是使用rtsf的主要工作

```
# 示例:
from rtsf.p_executer import Runner
class SubRunner(Runner):      
    
    def __init__(self):
        super(SubRunner,self).__init__()        
        
    def run_test(self, testcase_dict, driver_map):
        fn, _ = driver_map
        tracer = self.tracers[fn]
        parser = self.parser
        
```
- run_test(testcase_dict, driver_map), rtsf在执行测试的时候，调用run_test方法，传入testcase_dict和driver_map
- testcase_dict参数，是当前要执行的测试用例，rtsf将会传入字典格式
- driver_map参数，是当前要执行的设备，rtsf将会传入一个列表，格式如:("192.168.0.1:5555":selenium_driver), 默认情况下，("",None)
- self.parser,Runner中继承的属性， 解析测试用例的实例，控制全局上下文和映射关键字与执行函数
- self.tracers,Runner中继承的属性, 跟踪设备执行日志的实例，详细记录每个用例的执行过程

> 注意: 重写的时候，第一个参数，是单个case，不是所有case，**只需要写一个case的执行逻辑**

另外，使用rtsf,我这里已经写了几个项目,供大家参考和使用:

- [http/https自动化测试](https://github.com/RockFeng0/rtsf-http)
- [web ui自动化测试](https://github.com/RockFeng0/rtsf-web)
- [android ui自动化测试](https://github.com/RockFeng0/rtsf-app)
- 桌面客户端(WPF技术)自动化测试-敬请期待
- 桌面客户端(MFC技术)自动化测试-敬请期待


### TestRunner执行测试

- TestRunner(runner = Runner),runner参数用于指定重写了Runner.run_test的Runner子类,用于运行case,默认值为Runner
- TestRunner.run, 该方法用于运行指定yaml的case文件，或者运行指定文件夹路径中的yaml和json,如c:\case目录下*.yaml和*.json
- TestRunner。gen_html_report,方法用于生成测试报告，报告路径是yaml文件所在路径

```
# 示例:
# test.py
# coding:utf-8
from rtsf.p_executer import TestRunner,Runner

# 执行测试, 指定测试文件test.yaml
runner = TestRunner(runner = Runner).run('test.yaml')
# runner = TestRunner(runner = Runner).run(r'c:\case')

# 生成测试报告
html_report = runner.gen_html_report()

# 打印测试报告路径
print(html_report)

```


