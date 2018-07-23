# rock4

**[rock4automation项目](https://github.com/RockFeng0/rock4automation)痛点**
- 集成了 http测试,web UI测试，PC MFC UI测试，PC WPF UI测试，但实际上，QA或者测试人员，可能只需要http相关的api测试，却不得不将整个项目下载安装
- rock4automation项目,打包发布的程序，会将源码封装了exe或者加密为pyd；
- rock4automation项目,打包了相关工具，比如appium-server，java.exe 等等，大量冗余的，非项目源码的工具

**Rock4Test项目的目标**
- 可扩展，用于打造一个基本的测试服务框架,也许以后可以基于RPC，但是，目前，还只是一个可扩展的模块包
- 精简，拆分业务测试相关的功能、测试框架应有的基础功能、其他工具不再整合，Rock4Test项目，就是其中的基础功能
- 自成一体的执行逻辑，(yaml/excel/xml)测试用例->测试执行->跟踪日志->测试报告

## 测试用例模型

> 测试用例模型，计划扩展为, yaml, xml, excel三种，目前已扩展的只有yaml测试用例模型

### Yaml模型介绍

用例模型，基本保持[rock4automation项目](https://github.com/RockFeng0/rock4automation)的case模型

> 执行顺序  pre_command(List) -> steps(List) -> post_command(List) -> verify(List)

计划用例模板，为两个区域快:
- project区域快： name-待测系统的名称，module-测试集名称（一个文件就一个测试集合， 目前，还不支持测试套件的嵌套）
- case区域块：必填(id-测试用例id,desc-测试用例的描述,steps-测试步骤,verify-校验),选填(responsible-测试责任人,tester-测试执行人,pre_command-测试前置条件(前置钩子),post_command-测试后置条件(后置钩子))
- case区域块中，steps，计划分别支持(request-http测试，webdriver-web UI测试，mobiledriver-移动端app测试，wpfdriver-使用wpf技术的pc客户端测试，mfcdriver-使用mfc技术的pc客户端测试)


```
- project:
    name: xxx系统
    module: 登陆模块-功能测试
    
- case:
    id: xxx-1
    desc: 测试用例-格式设计
    responsible: 张三
    tester: 李四
    pre_command:
        - Set(passwd = "123456")
    steps:
        - request:
            url: http://www.baidu.com
            method: GET
            headers:
            data:
        - webdriver:
            by: css
            value: "#username"
            index: 0
            timeout: 10
            action: ${sendkey($username)}
        - webdriver:
            action: ${refresh}

        - mobiledriver:
            action: ${refresh}
            
        - wpfdriver:
            action: 
            
        - mfcdriver:
            actiion:
    post_command:
        - Set(passwd = "123456")
    verify:
        - VerifyCode("200")
```

## 测试执行方法

