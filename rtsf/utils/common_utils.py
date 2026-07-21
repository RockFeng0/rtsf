#! python3
# -*- encoding: utf-8 -*-

import os
import re
import sys
import inspect
import random
import string
import itertools

from collections import OrderedDict
from functools import reduce


class CommonUtils(object):

    @staticmethod
    def gen_random_string(str_len):
        return ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(str_len))

    @staticmethod
    def gen_cartesian_product(*args):
        if not args:
            return []
        elif len(args) == 1:
            return args[0]

        product_list = []
        for product_item_tuple in itertools.product(*args):
            product_item_dict = {}
            for item in product_item_tuple:
                product_item_dict.update(item)

            product_list.append(product_item_dict)

        return product_list

    @staticmethod
    def convert_to_order_dict(map_list):
        ordered_dict = OrderedDict()
        for map_dict in map_list:
            ordered_dict.update(map_dict)

        return ordered_dict

    @staticmethod
    def get_value_from_cfg(cfg_file):
        if not os.path.isfile(cfg_file):
            return

        cfg = {}
        import configparser
        config = configparser.RawConfigParser()

        try:
            config.read(cfg_file)
        except Exception as e:
            return
        for section in config.sections():
            cfg[section] = {}
            for option in config.options(section):
                cfg[section][option] = config.get(section, option)
        return cfg

    @staticmethod
    def get_sorted_list(ll):
        if not isinstance(ll, list):
            return ll

        re_digits = re.compile(r'(\d+)')

        def emb_numbers(s):
            pieces = re_digits.split(s)
            pieces[1::2] = map(int, pieces[1::2])
            return pieces

        return sorted(ll, key=emb_numbers)

    @staticmethod
    def get_exception_error():
        error_message = ""
        for i in range(len(inspect.trace())):
            error_line = u"""
        File:      %s - [%s]
        Function:  %s
        Statement: %s
        -""" % (inspect.trace()[i][1], inspect.trace()[i][2], inspect.trace()[i][3], inspect.trace()[i][4])

            error_message = "%s%s" % (error_message, error_line)

        error_message = u"""Error!\n%s\n\t%s\n\t%s\n""" % (error_message, sys.exc_info()[0], sys.exc_info()[1])
        error_message = error_message + "-" * 90 + "\n\n"
        return error_message


def seqfy(strs):
    if not strs:
        return

    result = ""
    seq = 1
    ss = strs.split("\n")
    for i in ss:
        if i:
            result = "".join([result, str(seq), ".", i, "\n"])
            seq = seq + 1
    return result


def unseqfy(strs):
    if not strs:
        return

    result = ""
    ss = strs.split("\n")
    for i in ss:
        raw = i.split(".", 1)
        if len(raw) == 2:
            try:
                int(raw[0])
            except ValueError:
                result = "".join([result, i, "\n"])
            else:
                result = "".join([result, raw[1], "\n"])
        else:
            result = "".join([result, raw[0], "\n"])

    return result


def stepfy(strs):
    result = {}
    prog_step = re.compile(r"^\d+\.")

    if not strs:
        return result

    raws = strs.split("\n")
    for raw in raws:
        step_num = raws.index(raw) + 1
        raw = prog_step.sub("", raw)
        if raw:
            result["Step_%s_info" % step_num] = raw
    return result


def unstepfy(sdict):
    if not sdict:
        return ""

    if not isinstance(sdict, dict):
        return sdict

    result = []
    for k, v in sdict.items():
        num = k.split("_")[1]
        result.append("%s.%s\n" % (num, v))

    if result:
        tmp = CommonUtils.get_sorted_list(result)
        f = lambda x, y: x + y

        return reduce(f, tmp)


def map_function(func_str, fw_action_addtion=None, bw_action_addtion=None, alias_func=None):
    split_action_value = re.compile(r"^(\w+)(\((.*)\)$)?")
    matched = split_action_value.match(func_str)

    if matched:
        action = matched.group(1).lower()
        value = matched.group(2)

        if alias_func:
            action = alias_func
        if fw_action_addtion:
            action = fw_action_addtion + action
        if bw_action_addtion:
            action = action + bw_action_addtion

        if value:
            return action + value
        else:
            return action
