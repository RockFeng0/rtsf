#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_tracer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_tracer,  v1.0 2018年7月2日
    FROM:   2018年7月2日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,os
from rtsf.p_tracer import Tracer

class TestTracer(unittest.TestCase):
    
    def setUp(self):
        self.results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_tmp")        
        self.app_log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_tmp","applog.log")
    
    def test_all_func(self):
        tracer = Tracer(logger_name = "case_log", dir_name = self.results_path)
        tracer.start(module_name="Test", case_name="case1", resp_tester='张三', tester='李四')    
        tracer.section("场景1")
        tracer.normal("网络信号状态测试")
        tracer.step("执行 步骤一")    
        tracer.ok("信号满载")
        tracer.fail("信号老差了")
        tracer.error("网络大姨妈来了")
        tracer.stop()
    
    def test_app_log_with_screen_handler(self):
        tracer = Tracer(logger_name = "app_log1", results_path = self.results_path)
        tracer.setup_logger("debug", logger_name = "app_log1")
        
        tracer.log_debug("默认的调试信息")
        tracer.log_info("虚惊一场，提示信息")
        tracer.log_warning("尼玛 报了警告")
        tracer.log_error("靠，又一个小错误")
        tracer.log_critical("尼玛 报了严重的错误")
        
        self.assertEqual(len(tracer.logger.handlers), 1)
    
    def test_app_log_with_file_handler(self):
        tracer = Tracer(logger_name = "app_log2", results_path = self.results_path)
        tracer.setup_logger("debug", log_file=self.app_log_file, logger_name = "app_log2")
        
        tracer.log_debug("默认的调试信息")
        tracer.log_info("虚惊一场，提示信息")
        tracer.log_warning("尼玛 报了警告")
        tracer.log_error("靠，又一个小错误")
        tracer.log_critical("尼玛 报了严重的错误")
        
        self.assertEqual(len(tracer.logger.handlers), 1)

    
if __name__ == "__main__":
    unittest.main(verbosity = 2)