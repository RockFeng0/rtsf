# -*- encoding: utf-8 -*-
'''
Current module: common.p_compat

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      common.p_compat,v 1.0 2018年5月26日
    FROM:   2018年5月26日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

try:
    import simplejson as json
except ImportError:
    import json

# ---------
# Specifics
# ---------

if is_py2:
    from urllib3.packages.ordered_dict import OrderedDict
    import ConfigParser
    reduce = reduce
    
    builtin_str = str
    bytes = str
    str = unicode      
    basestring = basestring
    numeric_types = (int, long, float)
    integer_types = (int, long)
    
    xrange = xrange

elif is_py3:
    
    from collections import OrderedDict
    import configparser as ConfigParser
    from functools import reduce
    
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)
    integer_types = (int,)
    
    xrange = range
