#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rtsf.test

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      rtsf.test,  v1.0 2019年2月27日
    FROM:   2019年2月27日
********************************************************************
======================================================================

Provide a function for the automation test

'''
# encoding:utf-8

from rtsf.p_executer import TestRunner, Runner

def test_add(x, y):
    global result
    result = x+y
    
def test_mod(x, y):
    global result
    result = x%y

def verify_is(x):
    return result == x    

class DemoRunner(Runner):      
    
    def __init__(self):
        ''' 继承Runner
        self._default_devices --> list,分布式设备标识。 默认 值 [""]，表示本机
        self._default_drivers --》 list, 分布式driver标识与driver键值对。 默认值 [("",None)]， 表示本机驱动
        self.parser --> TestCaseParser实例，用于解析用例
        self.tracers --> 每一台分布式设备初始化的Tracer实例，用于记录日志和生成报告       
        self.proj_info --> 记录了用例的项目信息 
        '''
        super(DemoRunner,self).__init__()
                
    def run_test(self, testcase_dict, variables, driver_map):
        ''' 重写 run_test，有三个参数
        @parm testcase_dict:  单条测试用例
        @param variables: dict; 用例采用数据驱动的情况下，variables是csv文件变量的笛卡儿积；默认情况下值是 {}
        @param driver_map:  tuple;  (唯一标识, driver or module or obj); 默认情况下的值是("",None),该参数适用于selenium的grid有多个 driver的情况
        '''
        
        # rtsf 遍历 self._default_drivers, 传给 driver_map   这里fn = ''  driver=None
        fn, driver = driver_map
        
        # 获取 fn 的跟踪对象， 用于记录日志 和 报告
        fn_logger = self.tracers[fn]
        
        # 获取用例解析对象
        parser = self.parser
        
        # 绑定测试用例关键字
        yaml_keys = {"add": test_add, "mod": test_mod, '_is': verify_is}
        parser.bind_functions(yaml_keys)        
        
        # 更新传入的变量
        parser.update_binded_variables(variables)
                
        # 获取用例名字  
        case_name = testcase_dict.get("name")        
        
        # parser.eval_content_with_bind_actions 用于解析 字段中的变量和函数，  如:  引用函数: ${function_str} 引用变量: $variable_str
        case_name = parser.eval_content_with_bind_actions(case_name)
        
        try:
            # fn_logger 可以记录报告，使用:  start, section, step, normal, ok, fail, error, stop
            # start 用于 开始记录报告；  stop 用于结束报告记录
            fn_logger.start(self.proj_info["module"],  # yaml case中 module
                            case_name,  # yaml case中 用例名臣
                            testcase_dict.get("responsible",u"administrator"), # yaml case中responsible定义的责任人名称 
                            testcase_dict.get("tester",u"administrator"), # yaml case中tester定义的测试人名称
                            )
            
            # fn_logger 可以使用了logging, 记录日志，使用:  log_debug, log_info, log_warning, log_error, log_critical
            fn_logger.log_debug(u"===== run_test\n\t{}".format(testcase_dict))
                     
            fn_logger.section(u"------------starting test")
            # 获取demotest
            demotest = testcase_dict.get("demotest")
            fn_logger.step("got demotest: %s" %demotest)
            
            parser.eval_content_with_bind_actions(demotest)                
            fn_logger.normal(u"eval demotest. finish")
            
            # 获取demoverify
            demoverify = testcase_dict.get("demoverify")
            fn_logger.step("got demoverify: %s" %demoverify)
            
            if parser.eval_content_with_bind_actions(demoverify):
                fn_logger.ok('verify is ok')
            else:
                fn_logger.fail('verify is fail')
            fn_logger.normal(u"eval demoverify. finish")            
            
        except Exception as e:
            fn_logger.error(e)
                             
        fn_logger.stop()
