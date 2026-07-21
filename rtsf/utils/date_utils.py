#! python3
# -*- encoding: utf-8 -*-

import time


class DateTimeUtils(object):

    @staticmethod
    def get_stamp_date():
        return time.strftime("%Y-%m-%d")

    @staticmethod
    def get_stamp_datetime():
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_stamp_datetime_coherent():
        return time.strftime("%Y-%m-%d_%H_%M_%S")
