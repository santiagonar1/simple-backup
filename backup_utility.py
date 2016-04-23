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
        self.size = None
        if os.path.isfile(self.path):
            self.size = os.path.getsize(self.path)
        elif os.path.isdir(self.path):
            self.size = sum([file.stat().st_size for file in self.scantree()])

    def exists(self):
        return os.path.exists(self.path)

    def scantree(self):
        """
        Permite iterar sobre todos los archivos dentro de la entrada. Esta DEBE ser un directorio
        """
        for entry in os.scandir(self.path):
            if entry.is_dir(follow_symlinks=False):
                yield from Entry(entry.path).scantree()
            else:
                yield entry

    def realpath(self, remove=''):
        rpath = os.path.dirname(self.path).replace(remove, '', 1)
        return rpath.replace(' ', '\\ ')

    def get_readable_size(self):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        nbytes = self.size
        if not nbytes:
            return '0 B'
        i = 0
        while nbytes >= 1000 and i < len(suffixes)-1:
            nbytes /= 1000
            i += 1
        f = ('%.1f' % nbytes)
        return  '{0:.1f} {1}'.format(nbytes, suffixes[i])

    def __eq__(self, other):
        return self.path == other.path

    def __ne__(self, other):
        return not self.__eq__(other)

class Backup:
    def __init__(self, entries, destiny):
        self.entries = entries[:]
        self.destiny = destiny.replace(' ', '\\ ')

    def start(self, use_common_path=True):
        commonpath = ''
        if use_common_path:
            commonpath = os.path.commonpath([f.path for f in self.entries])
            if commonpath == '/':
                commonpath = ''
        for entry in self.entries:
            dpath = self.destiny + entry.realpath(remove=commonpath)
            if not os.path.exists(dpath):
                os.makedirs(dpath)
            c = 'rsync -avz ' + entry.path.replace(' ','\\ ') + ' ' + dpath
            print(c)
            os.system(c)

def main():
    filepaths = ['/home/santiago/Documents/Presupuesto.ods',
             '/home/santiago/Documents/Shortcuts-linux.odt',
             '/home/santiago/Dropbox/Copias Importantes']
    entries = []
    for path in filepaths:
        entries.append(Entry(path))
    b = Backup(entries, '/tmp/Backup')
    b.start()
    return


if __name__ == '__main__':
    main()