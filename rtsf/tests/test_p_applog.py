#! python3
# -*- encoding: utf-8 -*-

import os
import unittest
from rtsf.p_applog import AppLog, color_print


class TestAppLog(unittest.TestCase):
    
    def setUp(self):
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_tmp", 'applog.log')
        if not os.path.exists(os.path.dirname(self.log_file)):
            os.makedirs(os.path.dirname(self.log_file))
                
    def test_log_with_file_handler(self):
        _applogobj = AppLog(logger_name="test1", log_file=self.log_file, log_level=10)
        logger = _applogobj.get_logger()
        
        logger.debug("debug ")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")
        
        self.assertTrue(os.path.exists(self.log_file))
        print('----')
        
    def test_log_with_screen_handler(self):      
        _applogobj = AppLog(logger_name="test2", log_level=10)
        logger = _applogobj.get_logger()
        
        logger.debug("debug ")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")
        
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