#! python3
# -*- encoding: utf-8 -*-

import os
import sys
import logging
from rtsf import p_exception

from colorama import Back, Fore, Style, init
from colorlog import ColoredFormatter
init(autoreset=True)


def coloring(msg, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    return fore_color + msg


def color_print(msg, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    print(fore_color + msg)


class AppLog(object):
    """ record the logs with your preference  """
    def __init__(self, logger_name=None):
        self.logger = logging.getLogger(logger_name)
        self.has_color = False
        self.formatter = logging.Formatter(u'%(asctime)s %(levelname)-8s: %(message)s')

    def setup_logger(self, log_level, log_file=None, has_color=False):
        """setup logger
            @param log_level: debug/info/warning/error/critical
            @param log_file: log file path
            @param has_color:
        """
        self.has_color = has_color
        level = getattr(logging, log_level.upper(), None)
        if not level:
            color_print("Invalid log level: %s" % log_level, "RED")
            sys.exit(1)
    
        # hide traceback when log level is INFO/WARNING/ERROR/CRITICAL
        if level >= logging.INFO:
            sys.tracebacklimit = 0
    
        if log_file:
            self._handle2file(log_file)
        self._handle2screen()
        
        self.logger.setLevel(level)
    
    @property
    def debug(self):
        return self._tolog("debug")
    
    @property
    def info(self):
        return self._tolog("info")
    
    @property
    def warning(self):
        return self._tolog("warning")
    
    @property
    def error(self):
        return self._tolog("error")
    
    @property    
    def critical(self):
        return self._tolog("critical")
    
    def _tolog(self, level):
        """ log with different level """
        def wrapper(msg):
            if self.has_color:
                color = self.log_colors[level.upper()]
                getattr(self.logger, level.lower())(coloring("- {}".format(msg), color))
            else:
                getattr(self.logger, level.lower())(msg)
    
        return wrapper
               
    def _handle2file(self, file_path):
        if os.path.isdir(os.path.abspath(os.path.dirname(file_path))):
            fh = logging.FileHandler(file_path, mode='a')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)    
            self.logger.addHandler(fh)
        else:
            raise p_exception.DirectoryNotFound(file_path)
    
    def _handle2screen(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        if self.has_color:
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
