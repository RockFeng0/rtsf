#! python3
# -*- encoding: utf-8 -*-

import os
import zipfile


class ZipUtils(object):

    @staticmethod
    def mkzip(source_dir, output_filename):
        zipf = zipfile.ZipFile(output_filename, 'w', zipfile.zlib.DEFLATED)
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)
                zipf.write(pathfile, arcname)
        zipf.close()

    @staticmethod
    def unzip(zipfilename, unziptodir):
        if not os.path.exists(unziptodir):
            os.mkdir(unziptodir)

        zfobj = zipfile.ZipFile(zipfilename)

        for z_info in zfobj.infolist():
            z_name = z_info.filename.replace('\\', '/')

            if z_info.flag_bits == 2048:
                ext_filename = os.path.join(unziptodir, z_name)
            else:
                ext_filename = os.path.join(unziptodir, z_name.encode('cp437').decode('gbk'))

            if z_name.endswith(os.sep):
                os.mkdir(ext_filename)
            else:
                ext_dir, ext_file = os.path.split(ext_filename)
                if not os.path.exists(ext_dir):
                    os.makedirs(ext_dir)

                if ext_file == '':
                    continue

                with open(ext_filename, 'wb') as f:
                    f.write(zfobj.read(z_name))
