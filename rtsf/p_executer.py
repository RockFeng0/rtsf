# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.p_executer

Rough version history:
v1.0    Original version to use
v1.1    add 'launch_mobile' function
********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:     rtsf.p_executer,v 2.0 2017年2月7日
    FROM:   2015年5月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import unittest,sys,os
from rtsf.p_applog import logger
from rtsf.p_tracer import Tracer
from rtsf.p_testcase import YamlCaseLoader
from rtsf import p_testcase, p_compat,p_exception

class TestCase(unittest.TestCase):
    """ create a testcase.
    """
    def __init__(self, test_runner, testcase_dict):
        super(TestCase, self).__init__()
        self.test_runner = test_runner
        self.testcase_dict = testcase_dict.copy()

    def runTest(self):
        """ run testcase and check result.
        """
        self.test_runner.run_test(self.testcase_dict)


class TestSuite(unittest.TestSuite):
    """ create test suite with a testset, it may include one or several testcases.
        each suite should initialize a separate Runner() with testset config.
    @param
        (dict) testset
            {
                "name": "testset description",
                "project": {
                    "name": "project name",
                    "module": "testset description"
                },
                "cases": [
                    {
                        "name": "testcase description",
                        "tester": "",    # optional
                        "responsible": "",    # optional
                        "pre_command": [],    # optional
                        "steps": [],      
                        "post_command": {},     # optional
                        "verify": []         # optional
                    },
                    testcase12
                ]
            }
    """
    def __init__(self, testset, runner_cls):
        super(TestSuite, self).__init__()
        
        file_path = testset.get("file_path")
        self.test_runner = test_runner = runner_cls()
        test_runner.init_runner(parser = p_testcase.TestCaseParser(file_path = file_path), 
                                tracer = Tracer(dir_name = os.path.dirname(os.path.abspath(file_path))),
                                projinfo = testset.get("project")
                                )
        
        testcases = testset.get("cases", [])
        for testcase_dict in testcases:
            self._add_test_to_suite(testcase_dict["name"], test_runner, testcase_dict.copy())


    def _add_test_to_suite(self, testcase_name, test_runner, testcase_dict):
        if p_compat.is_py3:
            TestCase.runTest.__doc__ = testcase_name
        else:
            TestCase.runTest.__func__.__doc__ = testcase_name

        test = TestCase(test_runner, testcase_dict)
        [self.addTest(test) for _ in range(int(testcase_dict.get("times", 1)))]
    
    @property
    def tests(self):
        return self._tests
   
class TaskSuite(unittest.TestSuite):
    """ create task suite with specified testcase path.
        each task suite may include one or several test suite.
    """
    def __init__(self, testsets, runner_cls):
        """
        @params
            testsets (dict/list): testset or list of testset
                testset_dict
                or
                [
                    testset_dict_1,
                    testset_dict_2,
                    {
                        "name": "desc1",
                        "config": {},
                        "api": {},
                        "testcases": [testcase11, testcase12]
                    }
                ]
            mapping (dict):
                passed in variables mapping, it will override variables in config block
        """
        super(TaskSuite, self).__init__()

        if not testsets:
            raise p_exception.TestcaseNotFound

        if isinstance(testsets, dict):
            testsets = [testsets]
        
        self.suite_list = []
        for testset in testsets:
            suite = TestSuite(testset, runner_cls)
            self.addTest(suite)
            self.suite_list.append(suite)

    @property
    def tasks(self):
        return self.suite_list


def init_test_suite(path_or_testsets, runner_cls):
    if not p_testcase.is_testsets(path_or_testsets):
        YamlCaseLoader.load_dependencies(path_or_testsets)        
        testsets = YamlCaseLoader.load_files(path_or_testsets)
    else:
        testsets = path_or_testsets

    return TaskSuite(testsets, runner_cls)

class TestRunner(object):

    def __init__(self, **kwargs):
        """ initialize test runner
        @param (dict) kwargs: key-value arguments used to initialize TextTestRunner            
        """
        runner_cls = kwargs.pop("runner", Runner)
        
        if not callable(runner_cls) and not isinstance(runner_cls(), Runner):
            raise p_exception.InstanceTypeError("Invalid runner, must be instance of Runner.")
        
        self._runner_cls = runner_cls
        self.runner = unittest.TextTestRunner(**kwargs)

    def run(self, path_or_testsets):
        """ start to run test with varaibles mapping
        @param path_or_testsets: YAML/JSON testset file path or testset list
            path: path could be in several type
                - absolute/relative file path
                - absolute/relative folder path
                - list/set container with file(s) and/or folder(s)
            testsets: testset or list of testset
                - (dict) testset_dict
                - (list) list of testset_dict
                    [
                        testset_dict_1,
                        testset_dict_2
                    ]
        """
                
        try:
            self._task_suite =init_test_suite(path_or_testsets, self._runner_cls)
        except p_exception.TestcaseNotFound:
            logger.log_error("Testcases not found in {}".format(path_or_testsets))
            sys.exit(1)

        self.text_test_result = self.runner.run(self._task_suite)        
        return self
    
    def gen_html_report(self):
        html_report = []
        for suite in self._task_suite.tasks:
            reporter = suite.test_runner.tracer
        
            proj_name = suite.test_runner.proj_info["name"]
            html_report.extend(reporter.generate_html_report(proj_name, proj_module=None))
        return html_report        
        
class Runner(object):
       
    def init_runner(self, parser, tracer, projinfo):
        self.parser = parser
        self.tracer = tracer
        self.proj_info = projinfo        
        
    def run_test(self, testcase_dict):
        ''' please override '''
        reporter = self.tracer
        reporter.start(self.proj_info["module"], testcase_dict.get("name",u'rtsf'), testcase_dict.get("responsible",u"rock feng"), testcase_dict.get("tester",u"rock feng"))
        reporter.log_debug(u"===== run_test\n\t{}".format(testcase_dict))
        
        reporter.section(u"------------section ok")
        reporter.step(u"step ok")
        reporter.normal(u"normal ok")
        reporter.stop()
