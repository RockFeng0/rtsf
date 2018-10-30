# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.p_executer

Rough version history:
v1.0    Original version to use
v1.1    add 'launch_mobile' function
v2.1    reconstitute this module with unittest and support mutil runner 
********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:     rtsf.p_executer,v 2.1 2018年9月2日
    FROM:   2015年5月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import unittest,sys,os
import multiprocessing,threading
from functools import partial
from rtsf.p_applog import logger
from rtsf.p_tracer import Tracer
from rtsf.p_testcase import YamlCaseLoader,parse_project_data
from rtsf import p_testcase, p_compat,p_exception

class TestCase(unittest.TestCase):
    """ create a testcase.
    """
    def __init__(self, test_runner, testcase_dict, variables):
        super(TestCase, self).__init__()
        self.test_runner = test_runner
        self.testcase_dict = testcase_dict.copy()
        self.variables = variables

    def runTest(self):
        """ run testcase and check result.
        """
        self.test_runner._run_test(self.testcase_dict, self.variables)


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
                    "data":[
                                {'csv': 'username_password.csv', 'by': 'Sequential'}, 
                                {'csv': 'devices.csv', 'by': 'Sequential'}
                            ]
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
         
        file_path    = testset.get("file_path")
        project      = testset.get("project")
        testcases    = testset.get("cases", [])        
        project_data = project.pop("data",[])
        
        test_runner = self.test_runner = runner_cls()
        if not isinstance(test_runner._default_devices, (list, tuple)):            
            raise TypeError("_default_devices not a list or tuple.")
        
        test_runner.init_runner(parser = p_testcase.TestCaseParser(file_path = file_path), 
                            tracers = {device:Tracer(device_id = device, dir_name = os.path.dirname(os.path.abspath(file_path))) for device in test_runner._default_devices},
                            projinfo = project
                            )
        
        for data_variables_dict in parse_project_data(project_data, file_path) or [{}]:
            for testcase_dict in testcases:                        
                self._add_test_to_suite(testcase_dict["name"], test_runner, testcase_dict, data_variables_dict)
                             
    def _add_test_to_suite(self, testcase_name, test_runner, testcase_dict, variables):
        if p_compat.is_py3:
            TestCase.runTest.__doc__ = testcase_name
        else:
            TestCase.runTest.__func__.__doc__ = testcase_name
        
        test = TestCase(test_runner, testcase_dict, variables)
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
            proj_name = suite.test_runner.proj_info["name"]
            reporters = suite.test_runner.tracers.values()
            
            for reporter in reporters:
                html_report.extend(reporter.generate_html_report(proj_name, proj_module=None))
        return html_report        
        
class Runner(object):
    
    def __init__(self):
        '''
        @note: maybe override variables
            _default_devices -> list type; to genrate tracer map, format is `{device_id: tracer_obj}`
                            e.g.
                                 default {"":tracer_obj} use to generate report for local host; 
                                 {"192.168.0.1:5555":tracer_obj1, "192.168.0.2:5555":tracer_obj2} use to generate report for remote host if run with mutilple process                                
            _default_drivers -> list type; to define driver map, format is `(device_id: driver)`
                            e.g.
                                default ("", None) use to run case with a driver;
                                [("192.168.0.1:5555":selenium_driver), ("192.168.0.2:5555":appium_driver), ...] use for multiple process to run case with specified drivers                      
        '''
        self._default_devices = [""]
        self._default_drivers = [("",None)]
        self._local_driver = True
    
    def init_runner(self, parser, tracers, projinfo):
        ''' initial some instances for preparing to run test case
        @note:  should not override
        @param parser: instance of TestCaseParser
        @param tracers: dict type for the instance of Tracer. Such as {"":tracer_obj} or {"192.168.0.1:5555":tracer_obj1, "192.168.0.2:5555":tracer_obj2} 
        @param proj_info: dict type of test case.  use like:  self.proj_info["module"], self.proj_info["name"]
            yaml case like: 
                - project:
                    name: xxx
                    module: xxxx
            dict case like:
                {"project": {"name": xxx, "module": xxxx}}            
                
        '''
        self.parser = parser
        self.tracers = tracers
        self.proj_info = projinfo
        
    def run_test(self, testcase_dict, variables, driver_map):
        ''' define how to run a case. override this method
        @param testcase_dice:  yaml case
        @param driver_map:  device id map to a driver 
              
        '''
        fn, _ = driver_map
        reporter = self.tracers[fn]
        
        parser = self.parser
        parser.update_binded_variables(variables)
        
        case_name = parser.eval_content_with_bind_actions(testcase_dict.get("name",u'rtsf'))
        reporter.start(self.proj_info["module"], case_name, testcase_dict.get("responsible",u"rock feng"), testcase_dict.get("tester",u"rock feng"))
        reporter.log_debug(u"===== run_test\n\t{}".format(testcase_dict))
        
        reporter.section(u"------------section ok")
        reporter.step(u"step ok")
        reporter.normal(u"normal ok")
        reporter.stop()
        
        return reporter
    
    def _run_test(self, testcase_dict, variables={}):
        ''' guide the running case
        @param testcase_dice:  yaml case
        @param variables: dict type; this is defined the variables for the data-driven test
                            e.g.
                                default {} use to run case without data-driven
                                {"username":"test1","password":"123456"}
        '''
        if self._local_driver:
            self.run_test(testcase_dict, variables, self._default_drivers[0])
        else:
            self._drivers = []
            self._run_grid_multithread(partial(self.run_test, testcase_dict, variables), self._default_drivers)
            
    def _run_grid_multiprocess(self, func, iterables):
        ''' running case with mutil process to support selenium grid-mode(multiple web) and appium grid-mode(multiple devices). 
        @param func:  function object
        @param iterables:  iterable objects
        '''
        multiprocessing.freeze_support()
        pool = multiprocessing.Pool()        
        pool_tracers = pool.map(func, iterables)
        pool.close()
        pool.join()
        
        # 传递给 pool.map的 实例对象，内存地址发生变化， 因此，这里在运行结束后，重新定义 self.tracers 
        self.tracers = dict(zip(self._default_devices, pool_tracers))
    
    def _run_grid_multithread(self, func, iterables):
        ''' running case with mutil process to support selenium grid-mode(multiple web) and appium grid-mode(multiple devices). 
        @param func:  function object
        @param iterables:  iterable objects
        '''
        
        f = lambda x: threading.Thread(target = func,args = (x,))
        threads = map(f, iterables)
        for thread in threads:
            thread.setDaemon(True)
            thread.start()
            thread.join()
            