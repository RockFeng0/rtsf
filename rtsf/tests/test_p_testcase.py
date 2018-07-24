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

import unittest
from rtsf.p_testcase import YamlCaseLoader, TestCaseParser

class TestYamlCaseLoader(unittest.TestCase):
    
    def test_load_file(self):        
        test_cases = YamlCaseLoader.load_file(r'data\case_model.yaml')
        self.assertIn("file_path", test_cases)
        self.assertIn("project", test_cases)
        self.assertIn("cases", test_cases)
            

class TestTestCaseParser(unittest.TestCase):
    
    def setUp(self):
        self._variables = {'v1':"hello", "v2":"world", "v3":123, "v4": 0.1234}
        self._functions = {"f1": lambda: "f1", "f2": lambda: "f2"}
        self._file_path = r'data\preference.py'
    
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
#     suite = unittest.TestSuite()
# #     suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTestCaseParser))
#     suite.addTest(TestTestCaseParser("test_eval_content_with_bind_actions_list_struct"))    
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)
    unittest.main(verbosity=2)