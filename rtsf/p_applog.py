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
    def __init__(self, logger_name=None, log_file=None, fmt=None, log_level=logging.DEBUG, has_color=False):
        self._logger = logging.getLogger(logger_name)
        self.has_color = has_color

        self.fmt = fmt if fmt else u"%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)-8s: %(message)s"
        # self.formatter = logging.Formatter(u'%(asctime)s %(levelname)-8s: %(message)s')
        self._format = logging.Formatter(self.fmt)

        # hide traceback when log level is INFO/WARNING/ERROR/CRITICAL
        if log_level >= logging.INFO:
            sys.tracebacklimit = 0

        # 添加文件日志
        if log_file:
            self.to_file(log_file)

        # 默认打印console日志
        self.to_console()
        self._logger.setLevel(log_level)

    def get_logger(self):
        return self._logger

    # @property
    # def debug(self):
    #     return self._tolog("debug")
    #
    # @property
    # def info(self):
    #     return self._tolog("info")
    #
    # @property
    # def warning(self):
    #     return self._tolog("warning")
    #
    # @property
    # def error(self):
    #     return self._tolog("error")
    #
    # @property
    # def critical(self):
    #     return self._tolog("critical")
    #
    # def _tolog(self, level):
    #     """ log with different level """
    #     def wrapper(msg):
    #         if self.has_color:
    #             color = self.log_colors[level.upper()]
    #             getattr(self._logger, level.lower())(coloring("- {}".format(msg), color))
    #         else:
    #             getattr(self._logger, level.lower())(msg)
    #
    #     return wrapper
               
    def to_file(self, file_path):
        """ 添加文件日志 记录Debug级别日志
        :return:
        """
        if os.path.isdir(os.path.abspath(os.path.dirname(file_path))):
            fh = logging.FileHandler(file_path, mode='a')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self._format)
            self._logger.addHandler(fh)
        else:
            raise p_exception.DirectoryNotFound(file_path)
    
    def to_console(self):
        """ 添加 控制台 日志， 打印Info级别日志
        :return:
        """
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # if self.has_color:
        #     self.log_colors = {
        #         'DEBUG':    'cyan',
        #         'INFO':     'green',
        #         'WARNING':  'yellow',
        #         'ERROR':    'red',
        #         'CRITICAL': 'red',
        #     }
        #
        #     color_formatter = ColoredFormatter(u"%(log_color)s%(bg_white)s#" + self.fmt,
        #         datefmt=None,
        #         reset=True,
        #         log_colors=self.log_colors
        #     )
        #
        #     ch.setFormatter(color_formatter)
        # else:
        #     ch.setFormatter(self._format)
        ch.setFormatter(self._format)
        self._logger.addHandler(ch)


if __name__ == '__main__':
    alg = AppLog(logger_name="TestApp1")
    console = alg.get_logger()
    console.debug("console debug")
    console.info("console info")
    console.warning("console warning")
    console.error("console error")
    alg.to_file(file_path=r"D:\auto\buffer\test_sdfsdf_20240403.log")
    console.debug("console debug - to file")
    console.info("console info - to file")
    console.warning("console warning - to file")
    console.error("console error - to file")

    logger = AppLog(logger_name="TestApp2", log_file=r"D:\auto\buffer\test_sdfsdf_20240403.log").get_logger()
    logger.debug("logger debug")
    logger.info("logger info")
    logger.warning("logger warning")
    logger.error("logger error")

