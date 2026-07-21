#! python3
# -*- encoding: utf-8 -*-

import os
import io
import json
import csv
import yaml

from rtsf import p_exception


class FileUtils(object):

    @staticmethod
    def _check_format(file_path, content):
        if not content:
            err_msg = u"Testcase file content is empty: {}".format(file_path)
            raise p_exception.FileFormatError(err_msg)

        elif not isinstance(content, (list, dict)):
            err_msg = u"Testcase file content format invalid: {}".format(file_path)
            raise p_exception.FileFormatError(err_msg)

    @staticmethod
    def _load_yaml_file(yaml_file):
        with io.open(yaml_file, 'r', encoding='utf-8') as stream:
            yaml_content = yaml.safe_load(stream)
            FileUtils._check_format(yaml_file, yaml_content)
            return yaml_content

    @staticmethod
    def _dump_yaml_file(data, yaml_file):
        with io.open(yaml_file, 'w', encoding='utf-8') as stream:
            yaml.dump(data, stream, allow_unicode=True)

    @staticmethod
    def _load_json_file(json_file):
        with io.open(json_file, encoding='utf-8') as data_file:
            try:
                json_content = json.load(data_file)
            except p_exception.JSONDecodeError:
                err_msg = u"JSONDecodeError: JSON file format error: {}".format(json_file)
                raise p_exception.FileFormatError(err_msg)

            FileUtils._check_format(json_file, json_content)
            return json_content

    @staticmethod
    def _load_csv_file(csv_file):
        csv_content_list = []

        with io.open(csv_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_content_list.append(row)

        return csv_content_list

    @staticmethod
    def load_file(file_path):
        if not os.path.isfile(file_path):
            raise p_exception.FileNotFoundError("{} does not exist.".format(file_path))

        file_suffix = os.path.splitext(file_path)[1].lower()
        if file_suffix == '.json':
            return FileUtils._load_json_file(file_path)
        elif file_suffix in ['.yaml', '.yml']:
            return FileUtils._load_yaml_file(file_path)
        elif file_suffix == ".csv":
            return FileUtils._load_csv_file(file_path)
        else:
            print(u"Unsupported file format: {}".format(file_path))
            return []

    @staticmethod
    def load_folder_files(folder_path, recursive=True, end_with=None):
        end_with = ('.yml', '.yaml', '.json') if end_with is None else end_with

        if isinstance(folder_path, (list, set)):
            files = []
            for path in set(folder_path):
                files.extend(FileUtils.load_folder_files(path, recursive))

            return files

        if not os.path.exists(folder_path):
            return []

        file_list = []

        for dirpath, dirnames, filenames in os.walk(folder_path):
            filenames_list = []

            for filename in filenames:
                if not filename.endswith(end_with):
                    continue

                filenames_list.append(filename)

            for filename in filenames_list:
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)

            if not recursive:
                break

        return file_list
