#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rtsf.tests.test_p_testcase

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      rtsf.tests.test_p_testcase,  v1.0 2018年7月19日
    FROM:   2018年7月19日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest, shutil,os
from rtsf.p_testcase import YamlCaseLoader, TestCaseParser, Yaml
from rtsf.p_common import FileSystemUtils


class TestYaml(unittest.TestCase):
        
    def test_load_folder_files(self):
        self.fp = r'data\testcases\t'
        p1 = r'data\testcases\t\t1'
        p2 = r'data\testcases\t\t2'
        FileSystemUtils.mkdirs(p1)
        FileSystemUtils.mkdirs(p2)
        shutil.copyfile(r'data\testcases\case_model.yaml', os.path.join(self.fp,"t.yaml"))
        shutil.copyfile(r'data\testcases\case_model.yaml', os.path.join(p1,"t1.yaml"))
        shutil.copyfile(r'data\testcases\case_model.yaml', os.path.join(p2,"t2.yaml"))
        
        result1 = Yaml.load_folder_files(self.fp, recursive = False)        
        self.assertEqual(len(result1), 1)
        
        result2 = Yaml.load_folder_files(self.fp, recursive = True)
        self.assertEqual(len(result2), 3)
        
class TestYamlCaseLoader(unittest.TestCase):
    
    def test_load_api_file(self):
        YamlCaseLoader.load_api_file(r'data\dependencies\api\api_model.yaml')
        
        self.assertEqual("test_api" in YamlCaseLoader.overall_def_dict["api"], True)
        self.assertEqual("function_meta" in YamlCaseLoader.overall_def_dict["api"]["test_api"], True)
    
    def test_load_dependencies_from_file(self):        
        YamlCaseLoader.load_dependencies(r'data\testcases\case_model.yaml')        
        self.assertEqual("test_api" in YamlCaseLoader.overall_def_dict["api"], True)
        self.assertEqual("function_meta" in YamlCaseLoader.overall_def_dict["api"]["test_api"], True)
        self.assertEqual("test_suite" in YamlCaseLoader.overall_def_dict["suite"], True)
        self.assertEqual("function_meta" in YamlCaseLoader.overall_def_dict["suite"]["test_suite"], True)
    
    def test_load_dependencies_from_dir(self):
        YamlCaseLoader.load_dependencies(r'data\testcases')
        self.assertEqual("test_api" in YamlCaseLoader.overall_def_dict["api"], True)
        self.assertEqual("function_meta" in YamlCaseLoader.overall_def_dict["api"]["test_api"], True)
        self.assertEqual("test_suite" in YamlCaseLoader.overall_def_dict["suite"], True)
        self.assertEqual("function_meta" in YamlCaseLoader.overall_def_dict["suite"]["test_suite"], True)
        
    def test_load_file(self):        
        test_cases = YamlCaseLoader.load_file(r'data\testcases\case_model.yaml')
        self.assertIn("file_path", test_cases)
        self.assertIn("project", test_cases)
        self.assertIn("cases", test_cases)
    
    def test_load_files_from_file(self):
        # file_abs_path.    Same as load_file
        test_cases = YamlCaseLoader.load_files(r'data\testcases\case_model.yaml')
        self.assertIn("file_path", test_cases[0])
        self.assertIn("project", test_cases[0])
        self.assertIn("cases", test_cases[0])
        
    def test_load_files_from_dir(self):        
        # file path.     
        fp = r'data\testcases\t'
        p1 = r'data\testcases\t\t1'
        p2 = r'data\testcases\t\t2'
        FileSystemUtils.mkdirs(p1)
        FileSystemUtils.mkdirs(p2)
        shutil.copyfile(r'data\testcases\case_model.yaml', os.path.join(fp,"t.yaml"))
        shutil.copyfile(r'data\testcases\case_model.yaml', os.path.join(p1,"t1.yaml"))
        shutil.copyfile(r'data\testcases\case_model.yaml', os.path.join(p2,"t2.yaml"))
        
        cases = YamlCaseLoader.load_files(r'data\testcases')
        self.assertEqual(len(cases), 4)
        
        all_cases_file_name = [os.path.basename(case["file_path"]) for case in cases]
        expected = ('case_model.yaml', "t.yaml", "t1.yaml", "t2.yaml")
        self.assertEqual(set(all_cases_file_name), set(expected))     
        

class TestTestCaseParser(unittest.TestCase):
    
    def setUp(self):
        self._variables = {'v1':"hello", "v2":"world", "v3":123, "v4": 0.1234}
        self._functions = {"f1": lambda: "f1", "f2": lambda: "f2"}
        self._file_path = r'data\testcases\preference.py'
    
    def test_init_variables(self):        
        
        parser = TestCaseParser(variables = self._variables, 
                                functions= self._functions,
                                file_path= self._file_path)
        
        # test variables
        for v in self._variables:
            self.assertEqual(v in parser._variables, True)
        
        # test file variables
        self.assertEqual(parser.get_bind_variable("test_var"), "hello world")
        
        # test functions
        for f in self._functions:
            self.assertEqual(f in parser._functions, True)
        
        # test file functions
        self.assertEqual(parser.get_bind_function("test_func")(), "nihao")
    
    
    def test_update_binded_variables(self):
        parser = TestCaseParser()
        parser.update_binded_variables(self._variables)
        
        # test variables
        for v in self._variables:
            self.assertEqual(v in parser._variables, True)
    
    def test_bind_functions(self):
        parser = TestCaseParser()
        parser.bind_functions(self._functions)
        
        # test functions
        for f in self._functions:
            self.assertEqual(f in parser._functions, True)
    
    def test_get_bind_variable(self):
        parser = TestCaseParser()
        parser.update_binded_variables(self._variables)
        
        self.assertEqual(parser.get_bind_variable("v1"), "hello")
        self.assertEqual(parser.get_bind_variable("v2"), "world")
        self.assertEqual(parser.get_bind_variable("v3"), 123)
        self.assertEqual(parser.get_bind_variable("v4"), 0.1234)
    
    def test_get_bind_function(self):
        parser = TestCaseParser()
        parser.bind_functions(self._functions)
        
        self.assertEqual(parser.get_bind_function("f1")(), "f1")
        
    def test_eval_content_with_bind_actions_normal_struct(self):
        parser = TestCaseParser(variables = self._variables, 
                                functions= self._functions,
                                file_path= self._file_path)
         
        normal_struct = "${f1()} say $v1 $v2,  preference.py set test_var to '$test_var' and test_func to '${test_func()}'"
        expect = "f1 say hello world,  preference.py set test_var to 'hello world' and test_func to 'nihao'"
        actual = parser.eval_content_with_bind_actions(normal_struct)
        self.assertEqual(actual, expect)
    
    def test_eval_content_with_bind_actions_list_struct(self):
        parser = TestCaseParser(variables = self._variables, 
                                functions= self._functions,
                                file_path= self._file_path)
         
        list_struct = ["$v1", "$v2", '${f1()}', "${f2()}", "$test_var", '${test_func()}']
        expect = ["hello", "world", "f1", "f2", "hello world", "nihao"]
        actual = parser.eval_content_with_bind_actions(list_struct)
        self.assertEqual(actual, expect)         
    
    def test_eval_content_with_bind_actions_dict_struct(self):
        parser = TestCaseParser(variables = self._variables, 
                                functions= self._functions,
                                file_path= self._file_path)
         
        dict_struct = {
            "variable": "$v1",
            "function": "${f1()}",
            "file_var": "$test_var",
            "file_func": "${test_func()}",
            }
         
        expect = {
            "variable": "hello",
            "function": "f1",
            "file_var": "hello world",
            "file_func": "nihao",
            }
        actual = parser.eval_content_with_bind_actions(dict_struct)
        self.assertEqual(actual, expect)       

if __name__ == '__main__':
    suite = unittest.TestSuite()
#     suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestYaml))
    suite.addTest(TestYamlCaseLoader("test_load_files_from_dir"))    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
#     unittest.main(verbosity=2)