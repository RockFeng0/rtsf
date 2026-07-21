#! python3
# -*- encoding: utf-8 -*-

from rtsf.utils.file_utils import FileUtils
from rtsf.utils.fs_utils import FileSystemUtils
from rtsf.utils.module_utils import ModuleUtils
from rtsf.utils.common_utils import CommonUtils, seqfy, unseqfy, stepfy, unstepfy, map_function
from rtsf.utils.date_utils import DateTimeUtils
from rtsf.utils.zip_utils import ZipUtils
from rtsf.utils.wait_utils import IntelligentWaitUtils
from rtsf.utils.progress_utils import ProgressBarUtils
from rtsf.utils.setup_utils import SetupUtils

import locale
import codecs
import sys
import os
import io
import time

filesystemencoding = sys.getfilesystemencoding()
encoding = "utf-8"
if sys.platform == 'win32':
    try:
        encoding = locale.getdefaultlocale()[1]
        codecs.lookup(encoding)
    except LookupError:
        pass
else:
    print("Waring: not window system.encoding is not setted.")
encoding = encoding.lower()


def init_project_env(subject='Automation', proj_path=None, sysencoding="utf-8", debug=False):
    if not proj_path:
        try:
            import inspect
            executable_file_path = os.path.dirname(os.path.abspath(inspect.stack()[-1][1]))
        except (IndexError, OSError):
            executable_file_path = os.path.dirname(sys.path[0])
        finally:
            proj_path = executable_file_path

    p = os.path.join(proj_path, subject)

    proj_conf = {
        "sys_coding": sysencoding,
        "debug": debug,
        "module_name": os.path.splitext(os.path.basename(subject))[0],
        "cfg_file": os.path.join(p, "config.ini"),
        "path": {"root": p,
                 "case": os.path.join(p, "testcase"),
                 "data": os.path.join(p, "data"),
                 "buffer": os.path.join(p, "buffer"),
                 "resource": os.path.join(p, "resource"),
                 "tools": os.path.join(p, "tools"),
                 "rst": os.path.join(p, "result"),
                 "rst_log": os.path.join(p, "result", "testcase"),
                 "rst_shot": os.path.join(p, "result", "screenshots"),
                 },
    }

    for v in proj_conf["path"].values():
        FileSystemUtils.mkdirs(v)
    sys.path.append(p) if os.path.isdir(p) else ""
    return proj_conf


ConfigParser = __import__('configparser').RawConfigParser
