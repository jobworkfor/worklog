# -*- coding: utf-8 -*-

import fileinput
import os
import shutil
import struct
import sys
import re
from src.util.helper_log import Log


class FileSystemHelper(object):
    def __init__(self):
        self.sep = os.path.sep
        pass

    def exists(self, path):
        return os.path.exists(path)

    def isDir(self, path):
        if path is None:
            return False
        return os.path.isdir(path)

    def isFile(self, path):
        if path is None:
            return False
        return os.path.isfile(path)

    def getcwd(self):
        return os.getcwd()

    def normpath(self, path):
        return os.path.normpath(path)

    def join(self, *pathSegment):
        path = "."
        for s in pathSegment:
            path = os.path.join(path, s)
        return path

    def realPath(self, path):
        '''
        derefences symbolic links, if b->a:
        >>> realpath('b')
        '/home/guest/play/paths/a'
        '''
        if path is None:
            return None
        if path.strip() is '':
            return None
        return os.path.realpath(path)

    def absPath(self, path):
        '''
        Won't derefences symbolic links, if b->a:
        >>> abspath('b')
        '/home/guest/play/paths/b'
        '''
        if path is None:
            return None
        if path.strip() is '':
            return None
        return os.path.abspath(path)

    def relativePath(self, basedir, path):
        if path is None:
            return None
        if not os.path.isdir(basedir):
            print("get_relative_path(), [%s] is not a valid directory" % basedir)
            return path

        path = self.abs_path(path)
        basedir = self.abs_path(basedir)
        relative_path = path.replace(basedir, '')
        while relative_path[0] == os.path.sep:
            relative_path = relative_path[1:]
        return relative_path

    def fileName(self, path):
        if path is None or not self.isFile(path):
            return None
        return os.path.basename(path)

    def dirName(self, path):
        if path is None:
            return None
        if os.path.isdir(path):
            directory = path
        else:
            directory = os.path.dirname(path)
        return directory

    def parentDir(self, path):
        if self.isFile(path):
            return os.path.abspath(os.path.dirname(os.path.dirname(path)))
        elif self.isDir(path):
            return os.path.abspath(os.path.dirname(path))
        else:
            return None

    def pwd(self, path, suffix=None):
        if suffix is not None:
            path = path + self.sep + suffix
        return os.path.split(self.absPath(path))[0]

    def touch(self, path):
        directory = os.path.dirname(path)

        if not os.path.isdir(directory):
            os.makedirs(os.path.dirname(path))

        f = open(path, 'a')
        f.close()

    def rm(self, path):
        if not self.exists(path):
            return

        if self.is_dir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def mv(self, from_path, dst_path, file_types=()):
        """
        :param from_path: from directory, eg. '/Users/Downloads/'
        :param dst_path: destination directory, eg. '/Users/Downloads/youtube/'
        :param file_types: file types which are intent to be moved, eg. '('.mp4', '.rmvb', '.MP4', 'RMVB')'
        :return: null
        """
        for f in os.listdir(from_path):
            if f.endswith(file_types):
                f_path = from_path + f
                d_path = dst_path

                print("moving [%s] from [%s] to [%s]" % (f, f_path, d_path))
                shutil.move(f_path, d_path)
        pass

    def cp(self, src, dst, print_info=False):
        if print_info:
            print("copying [%s] from [%s] to [%s]" % (src, src, dst))
        shutil.copyfile(src, dst)
        pass

    def searchFile(self, dir, regxStr):
        '''参数1要搜索的路径，参数2要搜索的文件名，可以是正则表代式'''
        matchedFile = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                if re.match(regxStr, file):
                    fname = os.path.abspath(os.path.join(root, file))
                    matchedFile.append(fname)
        return matchedFile

    def mkdirs(self, path):
        if self.isFile(path):
            path = os.path.dirname(path)
        os.makedirs(path)

    def tryGetFileType(self, filename):
        '''获取文件类型'''

        def fileTypes():
            '''
            支持文件类型
            用16进制字符串的目的是可以知道文件头是多少字节
            各种文件头的长度不一样，少则2字符，长则8字符
            :return:
            '''
            return {
                "FFD8FF": "JPEG",
                "89504E47": "PNG",
            }

        def bytes2hex(bytes):
            '''字节码转16进制字符串'''
            num = len(bytes)
            hexstr = u""
            for i in range(num):
                t = u"%x" % bytes[i]
                if len(t) % 2:
                    hexstr += u"0"
                hexstr += t
            return hexstr.upper()

        bin_file = open(filename, 'rb')  # 必需二制字读取
        knownTypes = fileTypes()
        ftype = 'unknown'
        for hex_code in knownTypes.keys():
            num_of_bytes = len(hex_code) / 2  # 需要读多少字节
            bin_file.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
            hbytes = struct.unpack_from("B" * num_of_bytes, bin_file.read(num_of_bytes))  # 一个 "B"表示一个字节
            f_hcode = bytes2hex(hbytes)
            if f_hcode == hex_code:
                ftype = knownTypes[hex_code]
                break
        bin_file.close()
        return ftype

    def deprecated_remove_the_first_line(self, path):
        swp_path = path + '.swp'
        removed_once = False

        first_line = ""
        with open(path, 'r') as f:
            with open(swp_path, 'w') as g:
                for line in f.readlines():
                    if removed_once:
                        g.write(line)
                    else:
                        first_line = line
                    removed_once = True

        shutil.move(swp_path, path)
        Log.i("remove line: " + str(first_line))

    def replase_file_content(self, path, line_num):
        for line in fileinput.input("filepath", inplace=1):
            line = line.replace("oldtext", "newtext")
        print(line)

    def file_content(self, path):
        file_object = open(path, 'r')
        try:
            all_the_text = file_object.read()
        finally:
            file_object.close()
        return all_the_text

    def search_file_text(self, path, word):
        for filename in os.listdir(path):
            fp = os.path.join(path, filename)
            if os.path.isfile(fp):
                with open(fp) as f:
                    for line in f:
                        if word in line:
                            break
            elif os.path.isdir(fp):
                self.search_file_text(fp, word)

    def text_line_num(self, filename):
        line_num = 0
        with open(filename) as todo_file:
            for _ in todo_file:
                line_num += 1
        return line_num

    def read_text_line(self, filename, line_no):
        fro = open(filename, "r")
        content = fro.readline()

        current_line = 0
        while current_line < line_no:
            content = fro.readline()
            current_line += 1
        return content

    def modify_text_line(self, filename, line_no, content):
        fro = open(filename, "r")

        current_line = 0
        while current_line < line_no:
            fro.readline()
            current_line += 1

        seek_point = fro.tell()

        frw = open(filename, "r+")
        frw.seek(seek_point, 0)

        # replace old line with content
        frw.writelines(str(content) + "\n")
        fro.readline()

        # now move the rest of the lines in the file one line back
        chars = fro.readline()
        while chars:
            frw.writelines(chars)
            chars = fro.readline()

        fro.close()
        frw.truncate()
        frw.close()

    def remove_the_first_line(self, filename, line_no):
        changed = False
        fro = open(filename, "r")

        current_line = 0
        while current_line < line_no:
            fro.readline()
            current_line += 1

        seekpoint = fro.tell()

        frw = open(filename, "r+")
        frw.seek(seekpoint, 0)

        # read the line we want to discard
        fro.readline()

        # now move the rest of the lines in the file one line back
        chars = fro.readline()
        while chars:
            frw.writelines(chars)
            chars = fro.readline()

        fro.close()
        frw.truncate()
        frw.close()

    def running_file_dir(self):
        """get the dir of calling script file"""
        path = sys.path[0]
        # check if the file is compiled and return the file path of each type of file
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    def getAndroidCodebaseTopDir(self, curDir):
        markFileName = "build/make/core/envsetup.mk"

        # check current dir first
        topDir = self.getcwd()
        markFilePath = self.join(topDir, markFileName)
        if self.exists(markFilePath):
            return topDir

        # check dir where bsbuild stay
        topDir = curDir
        while topDir != "/":
            print("--> ", topDir)
            markFilePath = self.join(topDir, markFileName)
            if self.exists(markFilePath):
                return topDir
            topDir = self.parentDir(topDir)

        return None
