#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Author: Santiago Narváez Rivas.
Date: 21-Apr-2016
"""
import os


class Entry:
    def __init__(self, path):
        self.path = path
        self.size = self.calc_size()

    def exists(self):
        return os.path.exists(self.path)

    def calc_size(self):
        size = None
        if os.path.isfile(self.path):
            size = os.path.getsize(self.path)
        elif os.path.isdir(self.path):
            size = sum([file.stat().st_size for file in self.scantree()])
        return size

    def scantree(self):
        """
        Permite iterar sobre todos los archivos dentro de la entrada. Esta DEBE ser un directorio
        """
        assert os.path.isdir(self.path)
        for entry in os.scandir(self.path):
            if entry.is_dir(follow_symlinks=False):
                yield from Entry(entry.path).scantree()
            else:
                yield entry

    def realpath(self, remove=''):
        return os.path.dirname(self.path).replace(remove, '', 1)

    def format_size(self):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        nbytes = self.size
        if not nbytes:
            return '0 B'
        i = 0
        while nbytes >= 1000 and i < len(suffixes)-1:
            nbytes /= 1000
            i += 1
        f = ('%.1f' % nbytes)
        return '%s %s' % (f, suffixes[i])

def main():
    entry = Entry('/home/santiago/Documents')
    print(entry.exists())
    print(entry.format_size())
    print(entry.realpath())
    return


if __name__ == '__main__':
    main()