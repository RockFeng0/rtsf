#! python3
# -*- encoding: utf-8 -*-
'''
Current module: rtsf.test

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      rtsf.test,  v1.0 2019年2月27日
    FROM:   2019年2月27日
********************************************************************
======================================================================

Provide a function for the automation test

'''
# encoding:utf-8

from rtsf.p_executer import TestRunner, Runner
    
runner = TestRunner().run('example_2.yaml')
runner.gen_html_report()