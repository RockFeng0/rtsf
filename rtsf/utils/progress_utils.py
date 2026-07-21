#! python3
# -*- encoding: utf-8 -*-

from functools import reduce


class ProgressBarUtils(object):

    @staticmethod
    def echo(transferred, toBeTransferred, suffix=''):
        bar_len = 60
        rate = transferred / float(toBeTransferred)

        filled_len = int(round(bar_len * rate))
        _percents = "%s%s" % (round(100.0 * rate, 1), "%")

        end_str = "\r"
        _bar = '=' * filled_len + '-' * (bar_len - filled_len)
        print("[%s] %s ...%s%s" % (_bar, _percents, suffix, end_str))

    def __init__(self, title, transferred=0.0, run_status=None, fin_status=None, toBeTransferred=100.0, unit='', sep='/', chunk_size=1.0):
        self.title = title
        self.toBeTransferred = toBeTransferred
        self.transferred = transferred
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def echo_size(self, transferred=1, status=None):
        self.transferred += transferred
        self.status = status or self.status
        end_str = "\r"
        if self.transferred == self.toBeTransferred:
            end_str = '\n'
            self.status = status or self.fin_status

        print(self.__get_info() + end_str)

    def echo_percent(self, transferred=1, status=None):
        self.transferred += transferred
        self.status = status or self.status
        end_str = "\r"
        if self.transferred == self.toBeTransferred:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_bar() + end_str)

    def __get_info(self):
        _title_info = "[%s] %s " % (self.title, self.status)
        _current_info = "%.2f %s " % (self.transferred / self.chunk_size, self.unit)
        _total_info = "%.2f %s" % (self.toBeTransferred / self.chunk_size, self.unit)

        _info = _title_info + _current_info + self.seq + _total_info
        return _info

    def __get_bar(self):
        _title_info = "[%s] %s " % (self.title, self.status)
        _rate = "%.2f%s" % (float(self.transferred) / float(self.toBeTransferred) * 100, "%")

        _info = _title_info + _rate + "=" * int(float(self.transferred) / float(self.toBeTransferred) * 50)
        return _info
