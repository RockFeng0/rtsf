# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.common

Rough version history:
v1.0    Original version to use
v2.0    Classify some useful functions 
v2.1    define this module for common functions
v3.0    delete the class of WebBasic 
        use this module instead of the class named WebBasic
v4.0    classify with  @staticmethod

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:    rtsf.p_common,v 4.0 2018年7月14日
    FROM:   2015年4月14日
********************************************************************
            
======================================================================

Frequently used package and functions.
'''


import locale
import codecs
import glob
import zipfile
import importlib
import types
import imp
import sys
import os
import io
import time
import re
import subprocess
import json
import inspect
import hashlib
import socket
import random
import string
import itertools
import csv
import yaml

from rtsf import p_compat, p_exception
from collections import OrderedDict

ConfigParser = p_compat.ConfigParser

filesystemencoding = sys.getfilesystemencoding()
encoding = "utf-8"
if sys.platform == 'win32':
    # Part code of IOBinding 
    try:
        encoding = locale.getdefaultlocale()[1]
        codecs.lookup(encoding)
    except LookupError:
        pass
else:
    print("Waring: not window system.encoding is not setted.")
encoding = encoding.lower()


# def set_sys_encode(code):
#     if p_compat.is_py2:    
#         import sys;reload(sys)
#         getattr(sys, "setdefaultencoding")(code)
#     else:
#         import importlib,sys
#         importlib.reload(sys)
        
def init_project_env(subject='Automation', proj_path = None, sysencoding = "utf-8", debug = False):
    ''' Set the environment for pyrunner '''    
        
#     if sysencoding:
#         set_sys_encode(sysencoding)
    
    if not proj_path:
        try:
            executable_file_path = os.path.dirname(os.path.abspath(inspect.stack()[-1][1]))
        except:
            executable_file_path = os.path.dirname(sys.path[0])
        finally:
            proj_path = executable_file_path
    
    p = os.path.join(proj_path,subject)
    
    proj_conf = {
        "sys_coding" : sysencoding,
        "debug" : debug,
        "module_name" : os.path.splitext(os.path.basename(subject))[0],
        "cfg_file" : os.path.join(p,"config.ini"),
        "path" : {"root" : p,
                  "case" : os.path.join(p,"testcase"),
                  "data" : os.path.join(p,"data"),
                  "buffer" : os.path.join(p,"buffer"),
                  "resource" : os.path.join(p,"resource"),
                  "tools" : os.path.join(p,"tools"),
                  "rst" : os.path.join(p,"result"),
                  "rst_log" : os.path.join(p,"result","testcase"),
                  "rst_shot" : os.path.join(p,"result","screenshots"),
            },
        }
     
    [FileSystemUtils.mkdirs(v) for v in proj_conf["path"].values()]    
    sys.path.append(p) if os.path.isdir(p) else ""
    return proj_conf

###  Common functions

class IntelligentWaitUtils(object):
    
    @staticmethod
    def until_cmd(listcmd, end_expects=None, save2logfile=None, coding = encoding):
        ''' 执行系统命令,并等待执行完
            @param listcmd: 执行的命令，列表格式
            @param end_expects: 命令执行结束，在输出的最后一行，正则搜素期望值，并设置 结果标志
            @param save2logfile:  设置执行过程，保存的日志
            @param coding: 设置输出编码        
        '''
        
        
        if end_expects and not isinstance(end_expects, p_compat.str):
            raise Exception("invalide unicode string: '%s'" %end_expects)
        
        lines = []    
        subp = subprocess.Popen(listcmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        while subp.poll()==None:
            next_line = subp.stdout.readline().decode(coding)
            if next_line:
#                 print(next_line)
                lines.append(next_line)
                if end_expects and re.search(end_expects, next_line):
                    result = True
                else:
                    result = False        
        subp.stdout.close()
        
        if subp.returncode:
            result = False
            lines.append("sub command error code: %s" %subp.returncode)
        
        if save2logfile:
            with open(save2logfile, 'a') as f:
                f.writelines(lines)
                                    
        return result
    
    @staticmethod
    def until(method, timeout = 30, message=''):
        """Calls the method until the return value is not False."""
        end_time = time.time() + timeout
        while True:
            try:
                value = method()
                if value:
                    return value
            except:
                pass            
            time.sleep(1)
            if time.time() > end_time:
                break
        raise Exception(message)
    
    @staticmethod
    def until_not(method, timeout = 30, message=''):
        """Calls the method until the return value is False."""
        end_time = time.time() + timeout
        while True:
            try:
                value = method()
                if not value:
                    return value
            except:
                return True
            time.sleep(1)
            if time.time() > end_time:
                break
        raise Exception(message)
    
    @staticmethod
    def wait_for_connection(ip="localhost",port=4444, timeout=30):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        end_time = time.time() + timeout
        while True:
            try:
                sk.connect((ip,int(port)))
                sk.shutdown(2)
                sk.close()
                return True    
            except:
                pass            
            time.sleep(1)
            if time.time() > end_time:
                break
        return False
        
class DateTimeUtils(object):
    
    @staticmethod
    def get_stamp_date():
        ''' Return the current date '''
        return time.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_stamp_datetime():
        ''' Return the current date time '''
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_stamp_datetime_coherent():
        ''' Return the current date time '''
        return time.strftime("%Y-%m-%d_%H_%M_%S")

class FileUtils(object):

    @staticmethod
    def _check_format(file_path, content):
        """ check testcase format if valid
        """
        if not content:
            # testcase file content is empty
            err_msg = u"Testcase file content is empty: {}".format(file_path)
            raise p_exception.FileFormatError(err_msg)

        elif not isinstance(content, (list, dict)):
            # testcase file content does not match testcase format
            err_msg = u"Testcase file content format invalid: {}".format(file_path)
            raise p_exception.FileFormatError(err_msg)

    @staticmethod
    def _load_yaml_file(yaml_file):
        """ load yaml file and check file content format
        """
        with io.open(yaml_file, 'r', encoding='utf-8') as stream:
            yaml_content = yaml.load(stream)
            FileUtils._check_format(yaml_file, yaml_content)
            return yaml_content

    @staticmethod
    def _load_json_file(json_file):
        """ load json file and check file content format
        """
        with io.open(json_file, encoding='utf-8') as data_file:
            try:
                json_content = json.load(data_file)
            except p_exception.JSONDecodeError:
                err_msg = u"JSONDecodeError: JSON file format error: {}".format(json_file)
                raise p_exception.FileFormatError(err_msg)

            FileUtils._check_format(json_file, json_content)
            return json_content

    @staticmethod
    def _load_csv_file(csv_file):
        """ load csv file and check file content format
        @param
            csv_file: csv file path
            e.g. csv file content:
                username,password
                test1,111111
                test2,222222
                test3,333333
        @return
            list of parameter, each parameter is in dict format
            e.g.
            [
                {'username': 'test1', 'password': '111111'},
                {'username': 'test2', 'password': '222222'},
                {'username': 'test3', 'password': '333333'}
            ]
        """
        csv_content_list = []

        with io.open(csv_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_content_list.append(row)

        return csv_content_list

    @staticmethod
    def load_file(file_path):
        if not os.path.isfile(file_path):
            raise p_exception.FileNotFoundError("{} does not exist.".format(file_path))

        file_suffix = os.path.splitext(file_path)[1].lower()
        if file_suffix == '.json':
            return FileUtils._load_json_file(file_path)
        elif file_suffix in ['.yaml', '.yml']:
            return FileUtils._load_yaml_file(file_path)
        elif file_suffix == ".csv":
            return FileUtils._load_csv_file(file_path)
        else:
            # '' or other suffix
            print(u"Unsupported file format: {}".format(file_path))
            return []

    @staticmethod
    def load_folder_files(folder_path, recursive=True):
        """ load folder path, return all files in list format.
        @param
            folder_path: specified folder path to load
            recursive: if True, will load files recursively
        """
        if isinstance(folder_path, (list, set)):
            files = []
            for path in set(folder_path):
                files.extend(FileUtils.load_folder_files(path, recursive))

            return files

        if not os.path.exists(folder_path):
            return []

        file_list = []

        for dirpath, dirnames, filenames in os.walk(folder_path):
            filenames_list = []

            for filename in filenames:
                if not filename.endswith(('.yml', '.yaml', '.json')):
                    continue

                filenames_list.append(filename)

            for filename in filenames_list:
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)

            if not recursive:
                break

        return file_list
    
class FileSystemUtils(object):
    
    @staticmethod
    def mkdirs(dir_path):
        ''' make a directory if it not exists'''
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    @staticmethod
    def getFileMd5(filePath):
        if not os.path.isfile(filePath):
            return
        myhash=hashlib.md5()
        with open(filePath,'rb') as f:
            while True:
                b=f.read(8096)
                if not b:
                    break;
                myhash.update(b)
        
        return myhash.hexdigest()
    
    @staticmethod
    def getFileSize(filePath):
        if not os.path.isfile(filePath):
            return
        else:
            return os.path.getsize(filePath)
        
    @staticmethod
    def get_legal_filename(fn):
        '''
        @param fn: file name
        @return: legal file name
        '''
        prog=re.compile(r"[\n\\/:*?\"<>|]")
        return prog.sub("",fn)
    
    @staticmethod
    def add_unique_postfix(fn):
        ''' 
        @param fn: File name
        @return:  Return an unique postfix for the file name                
        '''
        
        fn = p_compat.str(fn)
        
        if not os.path.exists(fn):
            return fn
        
        path, name = os.path.split(fn)
        name, ext = os.path.splitext(name)
        
        make_fn = lambda i: os.path.join(path, '%s_%d%s' % (name, i, ext))
        
        for i in p_compat.xrange(2, sys.maxsize):        
            uni_fn = make_fn(i)
            if not os.path.exists(uni_fn):            
                return uni_fn
        
        return None

    @staticmethod
    def force_delete_file(file_path):
        ''' force delete a file '''
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                return file_path
            except:           
                return FileSystemUtils.add_unique_postfix(file_path)
        else:
            return file_path
    
    
class ZipUtils(object):
    
    @staticmethod
    def mkzip(source_dir, output_filename):
        '''Usage:
            p = r'D:\auto\env\ttest\ins\build\lib\rock4\softtest\support'
            mkzip(os.path.join(p, "appiumroot"),os.path.join(p, "appiumroot.zip"))
            unzip(os.path.join(p, "appiumroot.zip"),os.path.join(p, "appiumroot2"))  
        '''
        zipf = zipfile.ZipFile(output_filename, 'w', zipfile.zlib.DEFLATED)
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep);#相对路径
                zipf.write(pathfile, arcname)
        zipf.close()
    
    @staticmethod
    def unzip(zipfilename, unziptodir):    
        if not os.path.exists(unziptodir): os.mkdir(unziptodir)
        
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            #name = name.replace('\\','/')
           
            if name.endswith(os.sep):
                os.mkdir(os.path.join(unziptodir, name))
            else:            
                ext_filename = os.path.join(unziptodir, name)
                ext_dir= os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir):   
                    os.makedirs(ext_dir)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
 
class ModuleUtils(object):
    
    @staticmethod
    def get_callable_class_method_names(testClass):
        '''
        @param testClass is a Class Object
        @return e.g.
            {"test": <function test at 0x03508B30>}
        '''
        isInstanceMethod = lambda attrname: not attrname.startswith("_") and hasattr(getattr(testClass, attrname), '__call__')
        methods = filter(isInstanceMethod, dir(testClass))                
        return {i : getattr(testClass,i) for i in methods}

    @staticmethod
    def is_function(tup):
        """ Takes (name, object) tuple, returns True if it is a function.
        """
        _, item = tup
        return isinstance(item, types.FunctionType)
    
    @staticmethod
    def is_variable(tup):
        """ Takes (name, object) tuple, returns True if it is a variable.
        """
        name, item = tup
        if callable(item):
            # function or class
            return False
        
        if isinstance(item, types.ModuleType):
            # imported module
            return False
        
        if name.startswith("_"):
            # private property
            return False
        
        return True
    
    @staticmethod
    def get_imported_module(module_name):
        """ import module and return imported module
        """
        return importlib.import_module(module_name)
    
    @staticmethod
    def get_imported_module_from_file(file_path):
        """ import module from python file path and return imported module
        """
        if p_compat.is_py3:
            imported_module = importlib.machinery.SourceFileLoader('module_name', file_path).load_module()
        elif p_compat.is_py2:
            imported_module = imp.load_source('module_name', file_path)
        else:
            raise RuntimeError("Neither Python 3 nor Python 2.")
    
        return imported_module
    
    @staticmethod
    def filter_module(module, filter_type):
        """ filter functions or variables from import module
        @params
            module: imported module
            filter_type: "function" or "variable"
        """
        filter_type = ModuleUtils.is_function if filter_type == "function" else ModuleUtils.is_variable
        module_functions_dict = dict(filter(filter_type, vars(module).items()))
        return module_functions_dict
    
    @staticmethod
    def search_conf_item(start_path, item_type, item_name):
        """ search expected function or variable recursive upward
        @param
            start_path: search start path
            item_type: "function" or "variable"
            item_name: function name or variable name
        e.g.
            search_conf_item('C:/Users/RockFeng/Desktop/s/preference.py','function','test_func')
        """
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
            # system root path
            err_msg = "'{}' not found in recursive upward path!".format(item_name)
            if item_type == "function":
                raise p_exception.FunctionNotFound(err_msg)
            else:
                raise p_exception.VariableNotFound(err_msg)
    
        return ModuleUtils.search_conf_item(dir_path, item_type, item_name)

class SetupUtils(object):
    
    @staticmethod
    def find_data_files(source,target,patterns,isiter=False):
        """Locates the specified data-files and returns the matches; 
            filesystem tree for setup's data_files in setup.py
            Usage:
                data_files = find_data_files(r"C:\Python27\Lib\site-packages\numpy\core","numpy/core",["*.dll","*.pyd"])
                data_files = find_data_files(r"d:\auto\buffer\test\test","buffer/test/test",["*"],True)
            :param source -a full path directory which you want to find data from
            :param target -a relative path directory which you want to pack data to
            :param patterns -glob patterns, such as "*dll", "*pyd"  etc.
            :param isiter - True/Fase, Will traverse path if True when patterns equal ["*"] 
        """
        if glob.has_magic(source) or glob.has_magic(target):
            raise ValueError("Magic not allowed in src, target")
        ret = {}
        for pattern in patterns:
            pattern = os.path.join(source,pattern)
            for filename in glob.glob(pattern):
                if os.path.isfile(filename):
                    targetpath = os.path.join(target,os.path.relpath(filename,source))
                    path = os.path.dirname(targetpath)
                    ret.setdefault(path,[]).append(filename)
                elif isiter and os.path.isdir(filename):
                    source2 = os.path.join(source,filename)
                    targetpath2 = "%s/%s" %(target,os.path.basename(filename))
                    # iter_target = os.path.dirname(targetpath2)
                    ret.update(SetupUtils.find_data_files(source2,targetpath2,patterns,isiter))
                 
        return sorted(ret.items())
    
class CommonUtils(object):
    
    @staticmethod
    def gen_random_string(str_len):
        return ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(str_len))
        
    @staticmethod
    def gen_cartesian_product(*args):
        """ generate cartesian product for lists,  笛卡尔积
        @param
            (list) args
                [{"a": 1}, {"a": 2}],
                [
                    {"x": 111, "y": 112},
                    {"x": 121, "y": 122}
                ]
        @return
            cartesian product in list
            [
                {'a': 1, 'x': 111, 'y': 112},
                {'a': 1, 'x': 121, 'y': 122},
                {'a': 2, 'x': 111, 'y': 112},
                {'a': 2, 'x': 121, 'y': 122}
            ]
        """
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
        """ convert mapping in list to ordered dict
        @param (list) map_list
            [
                {"a": 1},
                {"b": 2}
            ]
        @return (OrderDict)
            OrderDict({
                "a": 1,
                "b": 2
            })
        """
        ordered_dict = OrderedDict()
        for map_dict in map_list:
            ordered_dict.update(map_dict)
        
        return ordered_dict

    @staticmethod
    def get_value_from_cfg(cfg_file):
        ''' initial the configuration with file that you specify 
            Sample usage:            
                config = get_value_from_cfg()            
            return:
                return a dict        -->config[section][option]  such as config["twsm"]["dut_ip"]                
        '''    
    
        if not os.path.isfile(cfg_file):
            return
    
        cfg = {}   
        config = ConfigParser.RawConfigParser()
        
        try:
            config.read(cfg_file)
        except Exception as e:
    #         raise Exception("\n\tcommon exception 1.2: Not a well format configuration file. error: '%s'" %(e))
            return        
        for section in config.sections():
            cfg[section] = {}
            for option in config.options(section):
                cfg[section][option]=config.get(section,option)
        return cfg
    
    @staticmethod
    def get_exception_error():
        ''' Get the exception info
        Sample usage:
            try:
                raise Exception("asdfsdfsdf")
            except:
                print common.get_exception_error()
        Return:
            return the exception infomation.
        '''
        error_message = ""
        for i in range(len(inspect.trace())):
            error_line = u"""
        File:      %s - [%s]
        Function:  %s
        Statement: %s
        -""" % (inspect.trace()[i][1], inspect.trace()[i][2], inspect.trace()[i][3], inspect.trace()[i][4])
            
            error_message = "%s%s" % (error_message, error_line)    
        
        error_message = u"""Error!\n%s\n\t%s\n\t%s\n-------------------------------------------------------------------------------------------\n\n""" % (error_message,sys.exc_info()[0], sys.exc_info()[1])
        
        return error_message


class ProgressBarUtils(object):
    
    @staticmethod
    def echo(transferred, toBeTransferred, suffix=''):
        ''' usage:
            for i in range(101):
                ProgressBarUtils.echo(i,100)
        '''
        bar_len = 60                
        rate = transferred/float(toBeTransferred)
        
        filled_len = int(round(bar_len * rate))
        _percents = "%s%s" %(round(100.0 * rate, 1), "%")
        
        end_str = "\r"
        _bar = '=' * filled_len + '-' * (bar_len - filled_len)
        print("[%s] %s ...%s%s" %(_bar, _percents, suffix, end_str))
    
    def __init__(self, title, transferred=0.0, run_status=None, fin_status=None, toBeTransferred=100.0, unit='', sep='/', chunk_size=1.0):                   
        self.title = title
        self.toBeTransferred = toBeTransferred
        self.transferred = transferred
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep
            
    def echo_size(self, transferred=1, status=None):
        '''Sample usage:
            
            f=lambda x,y:x+y
            ldata = range(10)
            toBeTransferred = reduce(f,range(10))
            
            progress = ProgressBarUtils("refresh", toBeTransferred=toBeTransferred, unit="KB", chunk_size=1.0, run_status="正在下载", fin_status="下载完成")
            import time
            for  i in ldata:
                time.sleep(0.2)
                progress.echo_size(transferred=i)
        '''
        self.transferred += transferred
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.transferred == self.toBeTransferred:
            end_str = '\n'
            self.status = status or self.fin_status
        
        print(self.__get_info() + end_str)
        
    def echo_percent(self,transferred=1, status=None):
        '''Sample usage:
            f=lambda x,y:x+y
            ldata = range(10)
            toBeTransferred = reduce(f,range(10))
            
            import time
            progress = ProgressBarUtils("viewbar", toBeTransferred=toBeTransferred, run_status="正在下载", fin_status="下载完成")    
            for i in ldata:  
                time.sleep(0.1)  
                progress.echo_percent(i)
        '''
        self.transferred += transferred
        self.status = status or self.status
        end_str = "\r"
        if self.transferred == self.toBeTransferred:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_bar() + end_str)
    
    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _title_info = "[%s] %s " %(self.title, self.status)
        _current_info = "%.2f %s " %(self.transferred/self.chunk_size, self.unit)
        _total_info = "%.2f %s" %(self.toBeTransferred/self.chunk_size, self.unit)
        
        _info = _title_info + _current_info + self.seq + _total_info
        return _info
    
    def __get_bar(self):
        # 【名称】状态 进度 百分号 进度符号
        _title_info = "[%s] %s " %(self.title, self.status)
        _rate = "%.2f%s" %(float(self.transferred) / float(self.toBeTransferred) * 100, "%")
        
        _info = _title_info + _rate + "=" * int(float(self.transferred) / float(self.toBeTransferred) * 50)
        return _info

#### For testcases
def seqfy(strs):
    ''' 序列化 字符串--->实际效果是，为字符串，添加行号，返回字符串
    Sampe usage:
        strs = ["", None, u"First-line\nSecond-line\nThird-line", u"没有换行符"]
        for s in strs:
            print "---"
            result = seqfy(s)
            print result
            print unseqfy(result)
    '''
    
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
    ### 反序列化字符串--->实际效果是，去掉每行字符串前面的行号， 返回字符串
    if not strs:
        return
    
    result = ""   
    ss = strs.split("\n")
    for i in ss:
        raw = i.split(".",1)
        if len(raw) == 2:
            try:
                int(raw[0])
            except:
                result = "".join([result, i, "\n"])                    
            else:
                result = "".join([result, raw[1], "\n"])
        else:
            result = "".join([result, raw[0], "\n"])                
             
    return result

def stepfy(strs):
    ''' 步骤化 字符串 --->实际效果是, 依据 序列化的字符串，转换为 Step_%s_info 的字典， 返回字典
    Sample usage:
        test_strs = [
        "",
        None,
        u"First-line\nSecond-line\nThird-line",
        u'1.First-line\n2.Second-line\n3.Third-line\n',
        u'3.没有换行符',
        u'3.有换行符\n',
        "asdfasdfsdf",    
        "1.asdfasdfsdf\n2.sodfi",
        "1.1.dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n",
        "dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n",
        ]
        for i in test_strs:
            steps = stepfy(i)
            un = unstepfy(steps)
            print "string: %r" %i
            print "stepfy: %s" %steps
            print "unstepfy: %r\n" %un
    '''
    
    result = {}
    prog_step   = re.compile("^\d+\.")
      
    if not strs:
        return result
      
    raws = strs.split("\n")
    for raw in raws:
        step_num = raws.index(raw) + 1
        raw = prog_step.sub("",raw)       
        if raw:
            result["Step_%s_info" %step_num] = raw
    return result

def unstepfy(sdict):
    ### 反步骤化 字符串--->实际效果是, 依据 stepfy返回的字典数据，进行反步骤化，还原数据
    if not sdict:
        return ""
    
    if not isinstance(sdict, dict):
        return sdict
    
    result = []
    for k,v in sdict.items():
        num = k.split("_")[1]
        result.append("%s.%s\n" %(num,v))
    
    if result: 
        tmp = CommonUtils.get_sorted_list(result)    
        f = lambda x,y: x + y
                
        return p_compat.reduce(f, tmp)

def map_function(func_str, fw_action_addtion=None,bw_action_addtion=None, alias_func=None):
    ''' Sample usage:
        print map_function('set',alias_func = "ini_items");# -> ini_items
        print map_function('set',fw_action_addtion="action_steps_",bw_action_addtion="_for_upd",alias_func = "ini_items"); # -> action_steps_ini_items_for_upd
        print map_function('set(a=1,b=2,c=Test())',"action_steps_","_for_upd","ini_items");# -> action_steps_ini_items_for_upd(a=1,b=2,c=Test())
        print map_function('set("login",a="good",b=Test())',"action_steps_","_for_upd");# -> action_steps_set_for_upd("login",a="good",b=Test())
    '''
    
    split_action_value = re.compile("^(\w+)(\((.*)\)$)?")
    matched   = split_action_value.match(func_str)    
     
    if matched:
        action = matched.group(1).lower()
        value = matched.group(2)
        #params = matched.group(3)
        
        if alias_func:
            action = alias_func
        if fw_action_addtion:
            action = fw_action_addtion + action        
        if fw_action_addtion:
            action = action + bw_action_addtion
        
        if value:
            return action+value
        else:
            return action      

    
        

