#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Author: Santiago Narváez Rivas.
Date: 21-Apr-2016
"""
import os
import pwd


class File:
    def __init__(self, filepath):
        self.filepath = filepath

    def exists(self):
        return os.path.exists(self.filepath)

    def size(self):
        try:
            return os.path.getsize(self.filepath)
        except FileNotFoundError:
            return 0

    def realpath(self):
        homepath = '/home/' + pwd.getpwuid(os.getuid())[0] + '/'
        return os.path.dirname(self.filepath.replace(homepath, '', 1))


def main():
    file = File('/home/santiago/Documents/Presupuesto.ods')
    print(file.exists())
    print(file.size())
    print(file.realpath())
    return


if __name__ == '__main__':
    main()