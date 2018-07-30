# -*- encoding: utf-8 -*-
'''
Current module: common.p_exception

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      common.p_exception,v 1.0 2018年5月26日
    FROM:   2018年5月26日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import json

try:
    FileNotFoundError = FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

class MyBaseError(BaseException):
    pass

class FileFormatError(MyBaseError):
    pass

class ModelFormatError(MyBaseError):
    pass

class ParamsError(MyBaseError):
    pass

class ResponseError(MyBaseError):
    pass

class ParseResponseError(MyBaseError):
    pass

class ValidationError(MyBaseError):
    pass

class InstanceTypeError(MyBaseError):
    pass

class NotFoundError(MyBaseError):
    pass

class DirectoryNotFound(NotFoundError):
    pass

class FunctionNotFound(NotFoundError):
    pass

class VariableNotFound(NotFoundError):
    pass

class ApiNotFound(NotFoundError):
    pass

class SuiteNotFound(NotFoundError):
    pass

class TestcaseNotFound(NotFoundError):
    pass

