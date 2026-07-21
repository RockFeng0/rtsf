#! python3
# -*- encoding: utf-8 -*-

import os
import sys
import re
import hashlib


class FileSystemUtils(object):

    @staticmethod
    def mkdirs(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def get_file_md5(filePath):
        if not os.path.isfile(filePath):
            return
        myhash = hashlib.md5()
        with open(filePath, 'rb') as f:
            while True:
                b = f.read(8096)
                if not b:
                    break
                myhash.update(b)

        return myhash.hexdigest()

    @staticmethod
    def get_file_size(filePath):
        if not os.path.isfile(filePath):
            return
        else:
            return os.path.getsize(filePath)

    @staticmethod
    def get_legal_filename(fn):
        prog = re.compile(r"[\n\\/:*?\"<>|]")
        return prog.sub("", fn)

    @staticmethod
    def add_unique_postfix(fn):
        fn = str(fn)

        if not os.path.exists(fn):
            return fn

        path, name = os.path.split(fn)
        name, ext = os.path.splitext(name)

        make_fn = lambda i: os.path.join(path, '%s_%d%s' % (name, i, ext))

        for i in range(2, sys.maxsize):
            uni_fn = make_fn(i)
            if not os.path.exists(uni_fn):
                return uni_fn

        return None

    @staticmethod
    def force_delete_file(file_path):
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                return file_path
            except OSError:
                return FileSystemUtils.add_unique_postfix(file_path)
        else:
            return file_path
