#! python3
# -*- encoding: utf-8 -*-


from rtsf.p_report import HtmlReporter
from rtsf.p_applog import AppLog


class Tracer(HtmlReporter, AppLog):
    def __init__(self, **kwargs):
        self.__clear = False
        HtmlReporter.__init__(self, device_id=kwargs.get('device_id', ""), dir_name=kwargs.get('dir_name', ""))
        
        AppLog.__init__(self, logger_name=kwargs.get('logger_name'))
    
    def start(self,module_name, case_name, resp_tester, tester):
        if self.__clear:
            return
        self.start_test(module_name, case_name, resp_tester, tester)        
        self.log_info(u"-------\n\t#### Starting test {}: {} {} {}".format(module_name, case_name, resp_tester, tester))

    def section(self, strs):
        if self.__clear:
            return        
        self.step_info("section", self.__deal_str(strs))
        #self.log_info(self.__deal_str(strs))

    def normal(self, strs):
        if self.__clear:
            return        
        self.step_info("normal", self.__deal_str(strs))
        self.log_info(self.__deal_str(strs))

    def step(self, strs):
        if self.__clear:
            return
        self.step_info("step", self.__deal_str(strs))
        self.log_info(self.__deal_str(strs))

    def ok(self, strs):
        if self.__clear:
            return
        self.step_info("pass", self.__deal_str(strs))
        self.log_info(self.__deal_str(strs))

    def fail(self, strs):
        if self.__clear:
            return
        self.step_info("fail", self.__deal_str(strs))
        self.log_info(self.__deal_str(strs))

    def error(self, strs):
        if self.__clear:
            return
        self.step_info("error", self.__deal_str(strs))
        self.log_error(self.__deal_str(strs))

    def stop(self):
        if self.__clear:
            return
        self.stop_test()
        self.log_info(u"\n\t## Stopped test")
    
    def _switch_off(self):
        self.__clear = True
        
    def _switch_on(self):
        self.__clear = False
            
    def __deal_str(self,strs):
        if isinstance(strs, str):
            try:
                return strs.decode("utf-8")
            except:
                pass
        return strs    


tracer = Tracer()
