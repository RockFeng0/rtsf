#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rtsf.tests.test_p_executer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      rtsf.tests.test_p_executer,  v1.0 2018年7月19日
    FROM:   2018年7月19日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,os,shutil
from rtsf.p_executer import TestRunner,Runner,TaskSuite, TestSuite, init_test_suite
from rtsf.p_report import HtmlReporter
from rtsf.p_testcase import TestCaseParser
from rtsf.p_common import FileSystemUtils


class TestTestRunner(unittest.TestCase):
    
    def setUp(self):
        self.case = r'data\testcases\case_model.yaml'        
        self.testsets = {'file_path': 'C:\\d_disk\\auto\\git\\rtsf\\rtsf\\tests\\data\\testcases\\case_model.yaml', 
                    'project': {'name': 'xxx系统', 'module': '登陆模块-功能测试'}, 
                    'cases': [{'glob_var': {'passwd': '123@Qwe'}, 
                                'glob_regx': {'rex_name': 'id=su value=([\\w\\-\\.\\+/=]+)'}, 
                                'pre_command': ['${SetVar(username, luokefeng)}', '${SetVar(password, $passwd)}'], 
                                'steps': [{'request': {'url': 'https://www.baidu.com', 'method': 'GET'}}], 
                                'post_command': ['${DyStrData(baidu_name,$rex_name)}'], 
                                'verify': ['${VerifyCode(200)}', '${VerifyVar(baidu_name, 百度一下)}', '${VerifyVar(baidu_name, 123)}'], 
                                'name': 'ATP-1[打开百度]'
                                }, 
                                {'responsible': '罗科峰', 
                                 'tester': '罗科峰', 
                                 'pre_command': ['Set(passwd = "123456")'], 
                                 'steps': [{'request': {'url': 'https://www.baidu.com', 'method': 'GET', 'headers': None, 'data': None}}, {'webdriver': {'by': 'css', 'value': '#username', 'index': 0, 'timeout': 10, 'action': '${sendkey($username)}'}}, {'webdriver': {'action': '${refresh}'}}, {'mobiledriver': {'action': '${refresh}'}}, {'wpfdriver': {'action': None}}, {'mfcdriver': {'actiion': None}}], 
                                 'post_command': ['Set(passwd = "123456")'], 
                                 'verify': ['VerifyCode("200")'], 
                                 'name': 'ATP-2[测试用例-模板格式的设计-模板（全字段）]'
                                }
                            ], 
                    'name': '登陆模块-功能测试'
                    }
        self.testsets2 = self.testsets.copy()
        
    
    def test_init_test_suite_from_file(self):
        task_obj = init_test_suite(self.case, Runner)
        
        self.assertEqual(isinstance(task_obj, TaskSuite), True)
        self.assertEqual(len(task_obj.tasks), 1)
    
    def test_init_test_suite_from_dir(self):
        cases_path = r'test_tmp\testcases'
        p1 = os.path.join(cases_path, "t1")
        p2 = os.path.join(cases_path, "t2")
         
        FileSystemUtils.mkdirs(p1)
        FileSystemUtils.mkdirs(p2)
        shutil.copyfile(self.case, os.path.join(cases_path, "t.yaml"))
        shutil.copyfile(self.case, os.path.join(p1, "t1.yaml"))
        shutil.copyfile(self.case, os.path.join(p2, "t2.yaml"))
        
        task_obj = init_test_suite(cases_path, Runner)
        
        self.assertEqual(isinstance(task_obj, TaskSuite), True)  
        self.assertEqual(len(task_obj.tasks), 3)      
        
    def test_TaskSuite(self):        
        task_obj = TaskSuite([self.testsets, self.testsets2], Runner)        
        self.assertEqual(len(task_obj.tasks), 2)
    
    def test_TestSuite(self):
        suite_obj = TestSuite(self.testsets2, Runner)        
        self.assertEqual(len(suite_obj.tests), 2)
    
    def test_TestRunner_from_file(self):
#         logger.setup_logger("debug")
        runner = TestRunner(runner = Runner).run(self.case)
        html_report = runner.gen_html_report()
        #print(html_report)
          
        self.assertEqual(isinstance(runner.text_test_result, unittest.TextTestResult), True)
        self.assertEqual(isinstance(runner._task_suite, TaskSuite), True)
        self.assertEqual(len(runner._task_suite.tasks), 1)
        
          
        test_runner = runner._task_suite.tasks[0].test_runner        
        self.assertEqual(isinstance(test_runner, Runner), True)          
        self.assertEqual(isinstance(test_runner.tracer, HtmlReporter), True)
        self.assertEqual(isinstance(test_runner.parser, TestCaseParser), True)
          
        self.assertEqual(os.path.isfile(html_report[0]), True)
        
    def test_TestRunner_from_dir(self):
#         logger.setup_logger("debug")
        runner = TestRunner(runner = Runner).run(r'data\testcases')        
        html_report = runner.gen_html_report()        
        #print(html_report)
        
        self.assertEqual(isinstance(runner.text_test_result, unittest.TextTestResult), True)        
        self.assertEqual(isinstance(runner._task_suite, TaskSuite), True)
        self.assertEqual(len(runner._task_suite.tasks), 2)
        
        test_runner = runner._task_suite.tasks[0].test_runner        
        self.assertEqual(isinstance(test_runner, Runner), True)          
        self.assertEqual(isinstance(test_runner.tracer, HtmlReporter), True)
        self.assertEqual(isinstance(test_runner.parser, TestCaseParser), True)
        
        
        self.assertEqual(os.path.isfile(html_report[0]), True)
        self.assertEqual(os.path.isfile(html_report[1]), True)    
        
        
if __name__ == "__main__":
#     suite = unittest.TestSuite()
#     suite.addTest(TestTestRunner("test_TestRunner_from_dir"))    
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)    
    unittest.main()
    
    