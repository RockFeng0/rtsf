#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rock4.common.tests.test_p_executer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      rock4.common.tests.test_p_executer,  v1.0 2018年7月19日
    FROM:   2018年7月19日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,os
from rock4.common.p_executer import TestRunner,Runner
from rock4.common.p_report import HtmlReporter
from rock4.common.p_testcase import TestCaseParser


class TestTestRunner(unittest.TestCase):
    
    def test_run_and_gen_hetml_report(self):
#         logger.setup_logger("debug")
        runner = TestRunner(runner = Runner()).run(r'data\case_model.yaml')
        html_report = runner.gen_html_report()
        
        
        self.assertEqual(isinstance(runner.text_test_result, unittest.TextTestResult), True)
        self.assertEqual(isinstance(runner.test_runner, Runner), True)
        
        self.assertEqual(isinstance(runner.test_runner.tracer, HtmlReporter), True)
        self.assertEqual(isinstance(runner.test_runner.parser, TestCaseParser), True)
        
        self.assertEqual(os.path.isfile(html_report), True)
        
        
        
        
if __name__ == "__main__":
    unittest.main()