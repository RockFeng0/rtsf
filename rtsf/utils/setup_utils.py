#! python3
# -*- encoding: utf-8 -*-

import os
import glob


class SetupUtils(object):

    @staticmethod
    def find_data_files(source, target, patterns, isiter=False):
        if glob.has_magic(source) or glob.has_magic(target):
            raise ValueError("Magic not allowed in src, target")
        ret = {}
        for pattern in patterns:
            pattern = os.path.join(source, pattern)
            for filename in glob.glob(pattern):
                if os.path.isfile(filename):
                    targetpath = os.path.join(target, os.path.relpath(filename, source))
                    path = os.path.dirname(targetpath)
                    ret.setdefault(path, []).append(filename)
                elif isiter and os.path.isdir(filename):
                    source2 = os.path.join(source, filename)
                    targetpath2 = "%s/%s" % (target, os.path.basename(filename))
                    ret.update(SetupUtils.find_data_files(source2, targetpath2, patterns, isiter))

        return sorted(ret.items())
