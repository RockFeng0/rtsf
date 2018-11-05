#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rtsf.tests.test_p_report

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      rtsf.tests.test_p_report,  v1.0 2018年7月18日
    FROM:   2018年7月18日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import unittest, time
from rtsf.p_report import HtmlReporter

class TestHtmlReport(unittest.TestCase):    
        
    def test_add_report_data(self):
        result = []
        start_at = time.time()
        end_at = time.time() + 5
        result = HtmlReporter.add_report_data(result, case_name = 'test1', status = "Fail", resp_tester="administrator", tester = "tester1", start_at = start_at, end_at = end_at)
        result = HtmlReporter.add_report_data(result, case_name = 'test2', status = "Pass", resp_tester="administrator", tester = "tester2", start_at = start_at, end_at = end_at)
        result = HtmlReporter.add_report_data(result, module_name = "Module2", case_name = 'test1', status = "Fail", resp_tester="administrator", tester = "tester3", start_at = start_at, end_at = end_at)
        result = HtmlReporter.add_report_data(result, module_name = "Module2", case_name = 'test2', status = "Pass", resp_tester="administrator", tester = "tester4", start_at = start_at, end_at = end_at)
        result = HtmlReporter.add_report_data(result, case_name = 'test2', status = "Fail", resp_tester="administrator", tester = "tester2", start_at = start_at, end_at = end_at)
        
#         print(result)
        ''' result:
[{
    'Name': 'TestModule',
    'TestCases': [{
        'resp_tester': 'administrator',
        'tester': 'tester1',
        'case_name': 'test1',
        'status': 'Fail',
        'exec_date': '2018-07-18',
        'exec_time': '18: 18: 19',
        'start_at': 1531909099.781993,
        'end_at': 1531909104.781993
    },
    {
        'resp_tester': 'administrator',
        'tester': 'tester2',
        'case_name': 'test2',
        'status': 'Fail',
        'exec_date': '2018-07-18',
        'exec_time': '18: 18: 19',
        'start_at': 1531909099.781993,
        'end_at': 1531909104.781993
    }]
},
{
    'Name': 'Module2',
    'TestCases': [{
        'resp_tester': 'administrator',
        'tester': 'tester3',
        'case_name': 'test1',
        'status': 'Fail',
        'exec_date': '2018-07-18',
        'exec_time': '18: 18: 19',
        'start_at': 1531909099.781993,
        'end_at': 1531909104.781993
    },
    {
        'resp_tester': 'administrator',
        'tester': 'tester4',
        'case_name': 'test2',
        'status': 'Pass',
        'exec_date': '2018-07-18',
        'exec_time': '18: 18: 19',
        'start_at': 1531909099.781993,
        'end_at': 1531909104.781993
    }]
}]
        '''
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Name"], "TestModule")
        self.assertEqual(result[0]["TestCases"][1]["case_name"], "test2")
        self.assertEqual(result[0]["TestCases"][1]["status"], "Fail")
        
        self.assertEqual(result[1]["Name"], "Module2")
        
    def test_get_summary(self):
        result = [{'Name': 'TestModule', 'TestCases': [{'resp_tester': 'administrator', 'tester': 'tester1', 'case_name': 'test1', 'status': 'Fail', 'exec_date': '2018-07-18', 'exec_time': '18:18:19', 'start_at': 1531909099.781993, 'end_at': 1531909104.781993}, {'resp_tester': 'administrator', 'tester': 'tester2', 'case_name': 'test2', 'status': 'Fail', 'exec_date': '2018-07-18', 'exec_time': '18:18:19', 'start_at': 1531909099.781993, 'end_at': 1531909104.781993}]}, {'Name': 'Module2', 'TestCases': [{'resp_tester': 'administrator', 'tester': 'tester3', 'case_name': 'test1', 'status': 'Fail', 'exec_date': '2018-07-18', 'exec_time': '18:18:19', 'start_at': 1531909099.781993, 'end_at': 1531909104.781993}, {'resp_tester': 'administrator', 'tester': 'tester4', 'case_name': 'test2', 'status': 'Pass', 'exec_date': '2018-07-18', 'exec_time': '18:18:19', 'start_at': 1531909099.781993, 'end_at': 1531909104.781993}]}]        
        summary = HtmlReporter.get_summary(result, show_all = True, proj_name = "unit test", home_page = "http://github.com")
#         print(summary)

        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0]["project_name"], "unit test")
        self.assertEqual(summary[0]["module_name"], "TestModule")
        
        self.assertEqual(summary[1]["project_name"], "unit test")
        self.assertEqual(summary[1]["module_name"], "Module2")        
        
    def test_generate_html_report(self):        
        ####  same project name, different project module
        reporter = HtmlReporter()
        reporter.start_test("xxx功能模块1", "ATP-1【登录测试】-/index/login/1", "张三", "李四")
        reporter.step_info("section", "------------test_1")
        reporter.step_info("step","step1")
        reporter.step_info("normal","normal1")
        reporter.stop_test()
        
        reporter.start_test("xxx功能模块2", "ATP-2【登录测试】-/index/login/2", "张三", "李四")
        reporter.step_info("section", "------------test_1")
        reporter.step_info("step","step1")
        reporter.step_info("normal","normal1")
        reporter.stop_test()
        self.assertEqual(len(reporter.generate_html_report(proj_name = "xxx系统", proj_module = "xxx功能模块1")), 1)
        self.assertEqual(len(reporter.generate_html_report(proj_name = "xxx系统", proj_module = "xxx功能模块2")), 1)
        self.assertEqual(len(reporter.generate_html_report(proj_name = "xxx系统")), 2)
        
        
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestHtmlReport("test_generate_html_report"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
#     unittest.main()
    