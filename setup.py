#! python3
# -*- encoding: utf-8 -*-
'''
Current module: setup

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      setup,  v1.0 2018年7月23日
    FROM:   2018年7月23日
********************************************************************
======================================================================

Provide a function for the automation test

'''

from rock4 import __about__
from setuptools import find_packages, setup

install_requires = [
    "PyYAML",
    "Jinja2",
]

setup(
    name=__about__.__title__,
    version=__about__.__version__,
    description='basic test framwork for test',
    author=__about__.__autor__,
    author_email=__about__.__author_email__,
    url=__about__.HOME_PAGE,
    license=__about__.__license__,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    packages=find_packages(exclude=()),
    package_data={
        'rockr.common': ["templates/*"],
    },
    keywords='test unittest',
    install_requires=install_requires,
    extras_require={},    
)


