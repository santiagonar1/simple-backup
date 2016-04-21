#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Author: Santiago Narváez Rivas.
Date: 21-Apr-2016
"""
import os
import pwd


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

def main():
    entry = Entry('/home/santiago/Documents')
    print(entry.exists())
    print(entry.size)
    print(entry.realpath())
    return


if __name__ == '__main__':
    main()