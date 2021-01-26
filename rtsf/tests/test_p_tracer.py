#! python3
# -*- encoding: utf-8 -*-

import os
import unittest
from rtsf.p_tracer import Tracer
from rtsf.p_common import DateTimeUtils


class TestTracer(unittest.TestCase):
    
    def setUp(self):
        self.results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_tmp")
        self.app_log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_tmp", "applog.log")
    
    def test_all_func(self):
        tracer = Tracer(logger_name="case_log", dir_name=self.results_path)
            
        tracer.start(module_name="Test", case_name="case1", resp_tester='张三', tester='李四')    
        tracer.section("场景1")
        tracer.normal("网络信号状态测试")
        tracer.step("执行 步骤一")    
        tracer.ok("信号满载")
        tracer.fail("信号老差了")
        tracer.error("网络大姨妈来了")
        tracer.stop()
        
        expected_log = os.path.join(self.results_path, "report", "caselogs", u"%s_%s.log" %("case1", DateTimeUtils.get_stamp_date()))
        self.assertTrue(os.path.isfile(expected_log))
    
    def test_app_log_with_screen_handler(self):
        tracer = Tracer(logger_name="app_log1", dir_name=self.results_path)
        tracer.setup_logger("debug", logger_name="app_log1")
        
        tracer.log_debug("默认的调试信息")
        tracer.log_info("虚惊一场，提示信息")
        tracer.log_warning("尼玛 报了警告")
        tracer.log_error("靠，又一个小错误")
        tracer.log_critical("尼玛 报了严重的错误")
        
        self.assertEqual(len(tracer.logger.handlers), 1)
    
    def test_app_log_with_file_handler(self):
        tracer = Tracer(logger_name="app_log2", dir_name=self.results_path)
        tracer.setup_logger("debug", log_file=self.app_log_file, logger_name="app_log2")
        
        tracer.log_debug("默认的调试信息")
        tracer.log_info("虚惊一场，提示信息")
        tracer.log_warning("尼玛 报了警告")
        tracer.log_error("靠，又一个小错误")
        tracer.log_critical("尼玛 报了严重的错误")
        
        self.assertEqual(len(tracer.logger.handlers), 1)
        
    def test_no_trace(self):
        tracer = Tracer(logger_name="case_log", dir_name=self.results_path)
        tracer._switch_off()
        
        tracer.start(module_name="Test", case_name="case2", resp_tester='张三', tester='李四')    
        tracer.section("no log file")
        tracer.stop()
        
        not_expected_log = os.path.join(self.results_path, "report", "caselogs", u"%s_%s.log" % ("case2", DateTimeUtils.get_stamp_date()))
        self.assertFalse(os.path.isfile(not_expected_log))

    
if __name__ == "__main__":
    unittest.main(verbosity=2)
