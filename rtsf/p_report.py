# -*- encoding: utf-8 -*-
'''
Current module: rtsf.p_report2

Rough version history:
v1.0    Original version to use
v2.0    整合了跟踪日志和报告模块，跟踪记录执行步骤，记录日志，生成报告

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rtsf.p_report2,v 2.0 2018年7月18日
    FROM:   2017年2月14日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import os,time,codecs,io
from jinja2 import Template
from rtsf import p_compat
from rtsf.p_applog import logger
from rtsf.p_common import FileSystemUtils,DateTimeUtils
from rtsf import __about__

class HtmlReporter(object):
    def __init__(self,device_id="", dir_name = ''):       
        
        result_name = "report" if not device_id else "report_{}".format(device_id)
        result_path = dir_name if os.path.isdir(dir_name) else os.getcwd()
        
        self.result_path = os.path.join(result_path, result_name)
        self.case_log_path = os.path.join(self.result_path,"caselogs")
#         self.screen_shot_path = os.path.join(self.result_path,"screenshots")  
        self.summary = []      
                    
    def start_test(self,module_name,case_name, resp_tester, tester):
        '''
        @param module_name: test set name or test module name
        @param case_name: normal text case name, may contain '@#$~%^(+=-)&* ...'
        @param resp_tester: name of responsible tester
        @param tester: name of tester who run this case  
        '''
        self.meta_data = {
            "module_name": module_name,
            "raw_case_name": case_name,
            "case_name": FileSystemUtils.get_legal_filename(case_name),
            "status": "pass",
            "resp_tester":resp_tester,
            "tester":tester,
            "start_at": time.time(),
            "end_at":"",            
            }
        
        FileSystemUtils.mkdirs(self.case_log_path)
#         FileSystemUtils.mkdirs(self.screen_shot_path)
        
        log_file = self.__get_log_file()
        with codecs.open(log_file, "a", "utf-8") as f:
            f.write(u"\n**************  %s [%s]  ***************\n" %(u"Case Log From Rock4 Test Service Framework",self.meta_data['case_name']))
    
    def stop_test(self):
        self.meta_data["end_at"] = time.time()
        HtmlReporter.add_report_data(list_all = self.summary, **self.meta_data)
            
    def step_info(self, info, msg):
        
        if isinstance(msg, p_compat.bytes):            
            try:
                unicode_msg = msg.decode('utf-8')                
            except:
                raise Exception("Log message not unicode or utf-8.")
        else:
            unicode_msg = msg
        
        info = info.upper()
        log_file = self.__get_log_file()
        with codecs.open(log_file, "a", "utf-8") as f:
            if info == "SECTION":      
                f.write(u"\n%-20s\t%-10s\t%s\n" %(DateTimeUtils.get_stamp_datetime_coherent(),info, unicode_msg))
            elif info in ["NORMAL","STEP","PASS"]:
                f.write(u"%-20s\t%-10s\t%s\n" %(DateTimeUtils.get_stamp_datetime_coherent(),info,unicode_msg))
            elif info in ["ERROR","FAIL"]:
                f.write(u"%-20s\t%-10s\t%s\n" %(DateTimeUtils.get_stamp_datetime_coherent(),info,unicode_msg))
                self.meta_data["status"] = "Fail"
       
    
    def __get_log_file(self):
        log_file_name = u"%s_%s.log" %(self.meta_data['case_name'], DateTimeUtils.get_stamp_date())
        log_file = os.path.join(self.case_log_path,log_file_name)
        if not os.path.isfile(log_file):
            FileSystemUtils.mkdirs(self.case_log_path)
        return log_file 

    def generate_html_report(self, proj_name, proj_module = None):
        html_results = []               
        all_summary = HtmlReporter.get_summary(self.summary, proj_name = proj_name)
        
        for summary in all_summary:
            html_report = os.path.join(self.result_path, u"[{}]{}_{}.html".format(FileSystemUtils.get_legal_filename(summary["project_name"]),
                                                                                    FileSystemUtils.get_legal_filename(summary["module_name"]), 
                                                                                DateTimeUtils.get_stamp_datetime_coherent(),
                                                                                ))        
            if proj_module == None:                
                html_results.append(HtmlReporter.render_html(html_report, summary))
                
            elif summary["module_name"] == proj_module:
                html_results.append(HtmlReporter.render_html(html_report, summary))
                break
            else:
                summary = {}
        return html_results
    
    @staticmethod
    def render_html(report_file_path, summary):        
        html_report_template = os.path.join(os.path.abspath(os.path.dirname(__file__)),"templates","default_report_template.html")
        
        with io.open(html_report_template, "r", encoding='utf-8') as f_r:
            template_content = f_r.read()            
            with io.open(report_file_path, 'w', encoding='utf-8') as f_w:
                rendered_content = Template(template_content).render(summary)            
                f_w.write(rendered_content)
        
#         with open(os.path.join(os.path.dirname(report_file_path),'result.json'), 'w') as f:
#             f.write(str(summary.get("dict_report","")))
        
        return report_file_path
    
    @staticmethod
    def get_summary(list_all=[], **kwargs):
        ''' summarize the report data
            @param list_all: a list which save the report data
            @param kwargs: such as
                show_all:    True/False   report show all status cases
                proj_name:   project name 
                home_page:   home page url
        
        '''
        all_summary = []
               
        for module in list_all:
            summary = {
                        "module_name" : module['Name'],
                        "show_all" : kwargs.get("show_all",True),
                        "project_name" : kwargs.get("proj_name","TestProject"),
                        "home_page" : kwargs.get("home_page",__about__.HOME_PAGE),
                        "start_time" : "",
                        "end_time" : "",
                        "duration_seconds" : "",
                        "total_case_num" : len(module["TestCases"]),
                        "pass_cases_num" : 0,
                        "fail_cases_num" : 0,
                        "details" : []
                    }
                         
            for case in module["TestCases"]:
                case_detail = {}
                case_detail["linkurl"] =  "./caselogs/%s_%s.log" %(case["case_name"],case["exec_date"])
                
                if case["status"].lower() == "pass":
                    summary["pass_cases_num"] += 1
                    case_detail["c_style"] = "tr_pass"
                else:
                    summary["fail_cases_num"] += 1
                    case_detail["c_style"] = "tr_fail"
                
                case_detail.update(case)
            
                summary["details"].append(case_detail)                       
             
            try:
                st = module["TestCases"][0].get("start_at")
                et = module["TestCases"][-1].get("end_at")
                
                summary["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(st))    
                summary["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(et))        
                summary["duration_seconds"] = float("%.2f" %(et - st))
            except Exception as _:
                logger.log_warning("Will set 'start_at' and 'end_at' to 'None'")
                (summary["start_time"], summary["end_time"], summary["duration_seconds"]) = (None,None,None)
                    
            if summary["fail_cases_num"] > 0:
                summary["dict_report"] = {"result":0,"message":"failure","pass":summary["pass_cases_num"],"fail":summary["fail_cases_num"]}
            else:
                summary["dict_report"] = {"result":1,"message":"success","pass":summary["pass_cases_num"],"fail":summary["fail_cases_num"]}
             
            all_summary.append(summary)
            
        return all_summary
            
    @staticmethod
    def add_report_data(list_all=[], module_name="TestModule", **kwargs):
        ''' add report data to a list
            @param list_all: a list which save the report data
            @param module_name: test set name or test module name
            @param kwargs: such as
                case_name:   testcase name
                status:      test result, Pass or Fail
                resp_tester: responsible tester who write this case
                tester:      tester who execute the test
                start_at:    tester run this case at time 
                end_at:      tester stop this case at time
        '''
        start_at = kwargs.get("start_at")        
        case_name = kwargs.get("case_name","TestCase")
        raw_case_name = kwargs.get("raw_case_name","TestCase")
                
        exec_date_time = time.localtime(start_at)
        execdate = time.strftime("%Y-%m-%d",exec_date_time) 
        exectime = time.strftime("%H:%M:%S",exec_date_time)
        
        _case_report = {
                'resp_tester': kwargs.get("resp_tester","administrator"),
                'tester': kwargs.get("tester","administrator"),
                'case_name': case_name,
                'raw_case_name': raw_case_name,
                'status': kwargs.get("status","Pass"),
                'exec_date': execdate,
                'exec_time': exectime,
                'start_at': start_at,
                'end_at': kwargs.get("end_at"),
            }
                
        for module in list_all:
            if module_name != module["Name"]:
                continue
            
            for case in module["TestCases"]:
                if raw_case_name == case["raw_case_name"]:
                    case.update(_case_report)
                    return list_all
            
            module["TestCases"].append(_case_report)
            return list_all
        
        list_all.append({"Name": module_name, "TestCases": [_case_report]})
        return list_all


    
    




            
            