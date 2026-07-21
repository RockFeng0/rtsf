#! python3
# -*- encoding: utf-8 -*-

import os
import types
import importlib

from rtsf import p_exception


class ModuleUtils(object):

    @staticmethod
    def get_callable_class_method_names(testClass):
        is_instance_method = lambda attrname: not attrname.startswith("_") and hasattr(getattr(testClass, attrname), '__call__')
        methods = filter(is_instance_method, dir(testClass))
        return {i: getattr(testClass, i) for i in methods}

    @staticmethod
    def is_function(tup):
        _, item = tup
        return isinstance(item, types.FunctionType)

    @staticmethod
    def is_variable(tup):
        name, item = tup
        if callable(item):
            return False

        if isinstance(item, types.ModuleType):
            return False

        if name.startswith("_"):
            return False

        return True

    @staticmethod
    def get_imported_module(module_name):
        return importlib.import_module(module_name)

    @staticmethod
    def get_imported_module_from_file(file_path):
        spec = importlib.util.spec_from_file_location('module_name', file_path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        return imported_module

    @staticmethod
    def filter_module(module, filter_type):
        filter_type = ModuleUtils.is_function if filter_type == "function" else ModuleUtils.is_variable
        module_functions_dict = dict(filter(filter_type, vars(module).items()))
        return module_functions_dict

    @staticmethod
    def search_conf_item(start_path, item_type, item_name):
        dir_path = os.path.dirname(os.path.abspath(start_path))
        target_file = os.path.join(dir_path, "preference.py")

        if os.path.isfile(target_file):
            imported_module = ModuleUtils.get_imported_module_from_file(target_file)
            items_dict = ModuleUtils.filter_module(imported_module, item_type)
            if item_name in items_dict:
                return items_dict[item_name]
            else:
                return ModuleUtils.search_conf_item(dir_path, item_type, item_name)

        if dir_path == start_path:
            err_msg = "'{}' not found in recursive upward path!".format(item_name)
            if item_type == "function":
                raise p_exception.FunctionNotFound(err_msg)
            else:
                raise p_exception.VariableNotFound(err_msg)

        return ModuleUtils.search_conf_item(dir_path, item_type, item_name)
