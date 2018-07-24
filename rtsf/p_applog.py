# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.p_applog

Rough version history:
v1.0    Original version to use
v2.0    define some normal functions for this module which act as Log Center
********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:      rtsf.p_applog,v 2.0 2017年2月7日
    FROM:     2015年4月14日
********************************************************************
            
======================================================================

Provide a package for the log

'''

import os,logging,sys
from colorama import Back, Fore, Style, init
from colorlog import ColoredFormatter
init(autoreset=True)

from rtsf import p_exception


def coloring(msg, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    return fore_color + msg

def color_print(msg, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    print(fore_color + msg)
    
class AppLog(object):
    ''' record the logs with your preference  '''
    def __init__(self,logger_name = None):
        self.logger = logging.getLogger(logger_name)
        self.log_colors = {}        
        self.formatter = logging.Formatter(u'#%(asctime)s %(levelname)-8s: %(message)s')
    
    @staticmethod
    def setup_logger(log_level, log_file=None, logger_name=None):
        """setup logger
            @param log_level: debug/info/warning/error/critical
            @param log_file: log file path
            @param logger_name: the name of logger, default is 'root' if not specify
        """
        applogger = AppLog(logger_name)
        level = getattr(logging, log_level.upper(), None)
        if not level:
            color_print("Invalid log level: %s" % log_level, "RED")
            sys.exit(1)
    
        # hide traceback when log level is INFO/WARNING/ERROR/CRITICAL
        if level >= logging.INFO:
            sys.tracebacklimit = 0
    
        if log_file:
            applogger._handle2file(log_file)
        else:
            applogger._handle2screen(color = True)
        
        applogger.logger.setLevel(level)
    
    @property
    def log_debug(self):
        return self._tolog("debug")
    
    @property
    def log_info(self):
        return self._tolog("info")
    
    @property
    def log_warning(self):
        return self._tolog("warning")
    
    @property
    def log_error(self):
        return self._tolog("error")
    
    @property    
    def log_critical(self):
        return self._tolog("critical")
    
    def _tolog(self,level):
        """ log with different level """
        def wrapper(msg):
            if self.log_colors:
                color = self.log_colors[level.upper()]
                getattr(self.logger, level.lower())(coloring("- {}".format(msg), color))
            else:
                getattr(self.logger, level.lower())(msg)
    
        return wrapper
               
    def _handle2file(self,file_path):
        if os.path.isdir(os.path.abspath(os.path.dirname(file_path))):
            fh = logging.FileHandler(file_path, mode='a')          
            fh.setFormatter(self.formatter)    
            self.logger.addHandler(fh)
        else:
            raise p_exception.DirectoryNotFound(file_path)
    
    def _handle2screen(self, color = False):
        ch = logging.StreamHandler()
        
        if color:
            self.log_colors = {
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red',
            }
               
            color_formatter = ColoredFormatter(u"%(log_color)s%(bg_white)s#%(asctime)s %(levelname)-8s%(reset)s %(message)s",
                datefmt=None,
                reset=True,
                log_colors=self.log_colors
            )   
            
            ch.setFormatter(color_formatter)
        else:
            ch.setFormatter(self.formatter)
            
        self.logger.addHandler(ch)
          
logger = AppLog()