#! python3
# -*- encoding: utf-8 -*-

import os
import unittest
from rtsf.p_applog import AppLog, color_print


class TestAppLog(unittest.TestCase):
    
    def setUp(self):
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_tmp", 'applog.log')
                
    def test_log_with_file_handler(self):
        _applogobj = AppLog(logger_name="test1")
        _applogobj.setup_logger("debug", log_file=self.log_file, logger_name="test1")
        
        _applogobj.log_debug("debug ")
        _applogobj.log_info("info")
        _applogobj.log_warning("warning")
        _applogobj.log_error("error")
        _applogobj.log_critical("critical")
        
        self.assertEqual(_applogobj.log_colors, {})
        self.assertEqual(len(_applogobj.logger.handlers), 1)
        print('----')
        
    def test_log_with_screen_handler(self):      
        _applogobj = AppLog(logger_name="test2")
        _applogobj.setup_logger("debug", logger_name="test2")
        
        _applogobj.log_debug("debug ")
        _applogobj.log_info("info")
        _applogobj.log_warning("warning")
        _applogobj.log_error("error")
        _applogobj.log_critical("critical")
        
        self.assertEqual(_applogobj.log_colors, {})         
        self.assertEqual(len(_applogobj.logger.handlers), 1)
        print('----')
        
    def test_color_print(self):
        color_print('WHITE message')
        color_print('cyan message', 'cyan')
        color_print('red message', 'red')
        color_print('yellow message', 'yellow')
        color_print('green message', 'green')
        print('----')


if __name__ == "__main__":
    unittest.main(verbosity=2)
