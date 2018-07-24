#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rtsf.p_yaml_cases

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rtsf.p_testcase,v 1.0 2018年7月14日
    FROM:   2018年7月14日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import yaml
import json
import os,re,io,ast
from rtsf.p_applog import logger
from rtsf import p_exception,p_compat
from rtsf.p_common import FileSystemUtils,CommonUtils,ModuleUtils


variable_regexp = r"\$([\w_]+)"
function_regexp = r"\$\{([\w_]+\([\$\w\.\-_ =,]*\))\}"
function_regexp_compile = re.compile(r"^([\w_]+)\(([\$\w\.\-_ =,]*)\)$")

def extract_variables(content):
    """ extract all variable names from content, which is in format $variable
    @param (str) content
    @return (list) variable name list

    e.g. 
    print(extract_variables("abc")); # => []
    print(extract_variables("$variable")); # => ["variable"]
    print(extract_variables("http://$url")); # => ['url']
    print(extract_variables("/blog/$postid")); # => ["postid"]
    print(extract_variables("/$var1/$var2")); # => ["var1", "var2"]
    
    """
    try:
        return re.findall(variable_regexp, content)
    except TypeError:
        return []

def extract_functions(content):
    """ extract all functions from string content, which are in format ${fun()}
    @param (str) content
    @return (list) functions list

    e.g. 
    print(extract_functions('${func(5)}')); # => ["func(5)"]
    print(extract_functions('${func(a=1, b=2)}')); # => ["func(a=1, b=2)"]
    print(extract_functions('${func(a,b,c)}')); # => ['func(a,b,c)']
    print(extract_functions('/api/1000?_t=${get_timestamp()}')); # => ["get_timestamp()"]
    print(extract_functions('/api/${add(1, 2)}')); # => ["add(1, 2)"]
    print(extract_functions("/api/${add(1, 2)}?_t=${get_timestamp()}")); # => ["add(1, 2)", "get_timestamp()"]
    """
    try:
        return re.findall(function_regexp, content)
    except TypeError:
        return []

def parse_string_value(str_value):
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value

def parse_function(content):
    """ parse function name and args from string content.
    @param (str) content
    @return (dict) function name and args

    e.g. 
    print(parse_function("func()")); # => {'kwargs': {}, 'args': [], 'func_name': 'func'}
    print(parse_function("func(5)")); # => {'kwargs': {}, 'args': [5], 'func_name': 'func'}
    print(parse_function("func(a=1, b=2)")); # => {'kwargs': {'a': 1, 'b': 2}, 'args': [], 'func_name': 'func'}
    print(parse_function('func(a,b,c)')); # => {'kwargs': {}, 'args': ['a', 'b', 'c'], 'func_name': 'func'}
    """
    matched = function_regexp_compile.match(content)
    if not matched:
        raise p_exception.FunctionNotFound("{} not found!".format(content))

    function_meta = {
        "func_name": matched.group(1),
        "args": [],
        "kwargs": {}
    }

    args_str = matched.group(2).replace(" ", "")
    if args_str == "":
        return function_meta

    args_list = args_str.split(',')
    for arg in args_list:
        if '=' in arg:
            key, value = arg.split('=')
            function_meta["kwargs"][key] = parse_string_value(value)
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta

class TestCaseParser(object):
#     def __init__(self, action_class_name, preference_action_file):        
#         self._functions, self._variables = {}, {}
#         self.file_path = preference_action_file
#         _Actions = ModuleUtils.get_imported_module(action_class_name)                    
#         self.bind_functions(ModuleUtils.get_callable_class_method_names(_Actions.WebHttp))
#         self._variables = _Actions.WebHttp.glob
    
    def __init__(self, variables={}, functions={}, file_path=None):
        self._functions, self._variables = {}, {}
        self.update_binded_variables(variables)
        self.bind_functions(functions)
        self.file_path = file_path
                        
    def update_binded_variables(self, variables):
        """ bind variables to current testcase parser
        @param variable -> dict
            e.g.
            {"ip": "127.0.0.1"}
        """
        self._variables = variables

    def bind_functions(self, functions):
        """ bind functions to current testcase parser
        @param functions -> dict
            e.g.
            {"test": <function test at 0x03508B30>}
        """
        self._functions = functions
        
    def get_bind_variable(self, variable_name):
        '''
        @return: the value of variable_name
        '''
        return self._get_bind_item("variable", variable_name)
    
    
    def get_bind_function(self, func_name):
        '''
        @param func_name: function name
        @return: object of func_name
        '''
        return self._get_bind_item("function", func_name)
        
    def _get_bind_item(self, item_type, item_name):        
        
        if item_type == "function":            
            if item_name in self._functions:
                return self._functions[item_name]
            else:
                # is not keyword function, continue to search
                pass
        elif item_type == "variable":
            if item_name in self._variables:
                return self._variables[item_name]
        else:
            raise p_exception.ParamsError("bind item should only be function or variable.")

        try:
            # preference functions            
            assert self.file_path is not None
            return ModuleUtils.search_conf_item(self.file_path, item_type, item_name)
        except (AssertionError, p_exception.FunctionNotFound):
            raise p_exception.ParamsError(
                "{} is not defined in bind {}s!".format(item_name, item_type))
             
    def eval_content_with_bind_actions(self, content):
        """ parse content recursively, each variable and function in content will be evaluated.

        @param content =>  any data structure with ${func} or $variable
            
        """
        if content is None:
            return None

        if isinstance(content, (list, tuple)):
            return [self.eval_content_with_bind_actions(item) for item in content]

        if isinstance(content, dict):
            evaluated_data = {}
            for key, value in content.items():
                eval_key = self.eval_content_with_bind_actions(key)
                eval_value = self.eval_content_with_bind_actions(value)
                evaluated_data[eval_key] = eval_value

            return evaluated_data

        if isinstance(content, p_compat.basestring):

            # content is in string format here
            content = content.strip()

            # replace functions with evaluated value
            # Notice: _eval_content_functions must be called before _eval_content_variables
            content = self._eval_content_functions(content)

            # replace variables with binding value
            content = self._eval_content_variables(content)
        
        return content
    
    def _eval_content_functions(self, content):
        functions_list = extract_functions(content)
        for func_content in functions_list:
            function_meta = parse_function(func_content)
            func_name = function_meta['func_name']
            
            args = function_meta.get('args', [])
            kwargs = function_meta.get('kwargs', {})            
            args = self.eval_content_with_bind_actions(args)
            kwargs = self.eval_content_with_bind_actions(kwargs)

            func = self.get_bind_function(func_name)
            eval_value = func(*args, **kwargs)

            func_content = "${" + func_content + "}"
            if func_content == content:
                
                logger.log_debug("eval functions result: {} -> {}".format(func_content, eval_value))
                
                # content is a variable
                content = eval_value
            else:
                tmp = content
                
                # content contains one or many variables
                content = content.replace(
                    func_content,
                    p_compat.str(eval_value), 1
                )
                
                logger.log_debug("eval functions result: {} -> {}".format(tmp, content))
        
        return content
    
    def _eval_content_variables(self, content):
        variables_list = extract_variables(content)
        
        for variable_name in variables_list:
            variable_value = self.get_bind_variable(variable_name)
                        
            if "${}".format(variable_name) == content:
                logger.log_debug("eval variables result: ${} -> {}".format(variable_name, variable_value))
                # content is a variable                
                content = variable_value
            else:
                tmp = content
                                
                # content contains one or several variables
                content = content.replace("${}".format(variable_name),p_compat.str(variable_value), 1)
                
                logger.log_debug("eval variables result: {} -> {}".format(tmp, content))
                
        return content
    
class Yaml(object):

    @staticmethod
    def _check_format(file_path, content):
        """ check testcase format if valid
        """
        if not content:
            # testcase file content is empty
            err_msg = u"Testcase file content is empty: {}".format(file_path)
            logger.log_error(err_msg)
            raise p_exception.FileFormatError(err_msg)

        elif not isinstance(content, (list, dict)):
            # testcase file content does not match testcase format
            err_msg = u"Testcase file content format invalid: {}".format(file_path)
            logger.log_error(err_msg)
            raise p_exception.FileFormatError(err_msg)

    @staticmethod
    def _load_yaml_file(yaml_file):
        """ load yaml file and check file content format
        """
        with io.open(yaml_file, 'r', encoding='utf-8') as stream:
            yaml_content = yaml.load(stream)
            Yaml._check_format(yaml_file, yaml_content)
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
                logger.log_error(err_msg)
                raise p_exception.FileFormatError(err_msg)

            Yaml._check_format(json_file, json_content)
            return json_content
        
    @staticmethod
    def load_file(file_path):
        if not os.path.isfile(file_path):
            raise p_exception.FileNotFoundError("{} does not exist.".format(file_path))

        file_suffix = os.path.splitext(file_path)[1].lower()
        if file_suffix == '.json':
            return Yaml._load_json_file(file_path)
        elif file_suffix in ['.yaml', '.yml']:
            return Yaml._load_yaml_file(file_path)
        else:
            # '' or other suffix
            err_msg = u"Unsupported file format: {}".format(file_path)
            logger.log_warning(err_msg)
            return []



class YamlCaseLoader(object):            
    def translate(self):
        ''' usage:
            m = YamlCaseLoader(r"D:\auto\buffer\test.yaml")
            for i in m.translate():print(i)
        :return iterator (case_name, execute_function)
        '''
        if not self.check():
            return 
        
        for idx in range(len(self.testcases)):
            testing = self.testcases[idx]
            case_id = testing.get("testcaseid")
            case_name = FileSystemUtils.get_legal_filename("%s[%s]" %(case_id,p_compat.str(testing[self.__case_title_field])))
                         
            # executer actions
            execute_actionss = []
            for field in self.__executer_seq_fields:
                steps_info = testing.get(field)                                
                for execute_function in steps_info:
                    if not execute_function:
                        continue
                    execute_actionss.append(execute_function)                
            yield (case_name, execute_actionss, idx)
    
    def check(self):
        ''' usage:
            print(YamlModel(r"D:\auto\buffer\test.yaml").check()    )
        :return Ture/False
        '''
        result = True
        self.testcases,invalid_cases = self.getYamlCasesValue()
        if invalid_cases:
            print("Waring: Yaml need available fields:")
            for k,v in invalid_cases.items():
                print("\t%s -> %r" %(k, v))
            result = False
        elif not self.testcases:
            print('Warning: Invalid Yaml Test Model.')
            result = False
            
        return result
    
    @staticmethod
    def load_file(yaml_file):
        ''' load yaml file
        @param yaml_file: yaml file path
        @return: testset 
        
        '''
        testset = {
            "file_path": yaml_file,
            "project": {},
            "cases": [],
        }
        word_p = "^[\w-]+$"
        
        if not os.path.isfile(yaml_file):        
            raise p_exception.FileNotFoundError("Not found testcase file {}.".format(yaml_file))
        
        try:
            test_cases = Yaml.load_file(yaml_file)
            logger.log_debug("Yaml raw dict: {}".format(test_cases))
            
            for item in test_cases:
                if not isinstance(item, dict) or len(item) != 1:
                    raise p_exception.FileFormatError("Testcase format error: {}".format(yaml_file))
    
                key, test_block = item.popitem()
                if not isinstance(test_block, dict):
                    raise p_exception.FileFormatError("Testcase format error: {}".format(yaml_file))
    
                if key == "project":
                    testset["project"].update(test_block)
                    testset["name"] = test_block.get("module", "Default Test Set")
    
                elif key == "case":
                    case_id = test_block.pop("id","")
                    desc = test_block.pop("desc","")
                    if not case_id:
                        raise p_exception.ModelFormatError("Some cases do not have 'case_id'.")
                    if not re.search(word_p,case_id):
                        raise p_exception.ModelFormatError("Invalid case_id: {}".format(case_id))
                    
                    test_block["name"] = FileSystemUtils.get_legal_filename("%s[%s]" %(case_id, desc))                    
                    testset["cases"].append(test_block)
    
                else:
                    logger.log_warning("unexpected block key: {}. block key should only be 'project' or 'case'.".format(key))
            
        except:
            logger.log_error(CommonUtils.get_exception_error())
        finally:
            return testset
            
def is_testset(data_structure):
    """ check if data_structure is a testset
    testset should always be in the following data structure:
        {
            "name": "desc1",
            "project": {},
            "cases": [testcase11, testcase12]
        }
    """
    if not isinstance(data_structure, dict):
        return False

    if "name" not in data_structure or "cases" not in data_structure:
        return False

    if not isinstance(data_structure["cases"], list):
        return False

    return True

def is_testsets(data_structure):
    """ check if data_structure is testset or testsets
    testsets should always be in the following data structure:
        testset_dict
        or
        [
            testset_dict_1,
            testset_dict_2
        ]
    """
    if not isinstance(data_structure, list):
        return is_testset(data_structure)

    for item in data_structure:
        if not is_testset(item):
            return False

    return True



