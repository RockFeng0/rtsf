#! python3
# -*- encoding: utf-8 -*-

import re
import time
import socket
import subprocess


class IntelligentWaitUtils(object):

    @staticmethod
    def until_cmd(listcmd, end_expects=None, save2logfile=None, coding="utf-8"):
        if end_expects and not isinstance(end_expects, str):
            raise Exception("invalide unicode string: '%s'" % end_expects)

        lines = []
        result = False
        subp = subprocess.Popen(listcmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while subp.poll() == None:
            next_line = subp.stdout.readline().decode(coding)
            if next_line:
                lines.append(next_line)
                if end_expects and re.search(end_expects, next_line):
                    result = True
                else:
                    result = False
        subp.stdout.close()

        if subp.returncode:
            result = False
            lines.append("sub command error code: %s" % subp.returncode)

        if save2logfile:
            with open(save2logfile, 'a') as f:
                f.writelines(lines)

        return result

    @staticmethod
    def until(method, timeout=30, message=''):
        end_time = time.time() + timeout
        while True:
            try:
                value = method()
                if value:
                    return value
            except Exception:
                pass
            time.sleep(1)
            if time.time() > end_time:
                break
        raise Exception(message)

    @staticmethod
    def until_not(method, timeout=30, message=''):
        end_time = time.time() + timeout
        while True:
            try:
                value = method()
                if not value:
                    return value
            except Exception:
                return True
            time.sleep(1)
            if time.time() > end_time:
                break
        raise Exception(message)

    @staticmethod
    def wait_for_connection(ip="localhost", port=4444, timeout=30):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        end_time = time.time() + timeout
        while True:
            try:
                sk.connect((ip, int(port)))
                sk.shutdown(2)
                sk.close()
                return True
            except (ConnectionRefusedError, OSError):
                pass
            time.sleep(1)
            if time.time() > end_time:
                break
        return False
