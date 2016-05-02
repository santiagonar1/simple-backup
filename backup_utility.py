#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Author: Santiago Narváez Rivas.
Date: 21-Apr-2016
"""
import os
import threading
from observer import Observable


class Entry:
    def __init__(self, path):
        self.path = path
        self.size = None
        if self.is_file():
            self.size = os.path.getsize(self.path)
        elif os.path.isdir(self.path):
            self.size = get_tree_size(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

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


class Backup(threading.Thread, Observable):
    def __init__(self, entries, destiny, use_common_path=True):
        threading.Thread.__init__(self)
        Observable.__init__(self)
        self.entries = entries[:]
        self.destiny = destiny.replace(' ', '\\ ')
        self.use_common_path = use_common_path

    def run(self):
        commonpath = ''
        if self.use_common_path:
            commonpath = os.path.commonpath([f.path for f in self.entries])
            if commonpath == '/':
                commonpath = ''
        for entry in self.entries:
            dpath = self.destiny + entry.realpath(remove=commonpath)
            if not os.path.exists(dpath):
                os.makedirs(dpath)
            c = 'rsync -avz ' + entry.path.replace(' ','\\ ') + ' ' + dpath
            os.system(c)
            self.notify_observers(entry.path)

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

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

def string_to_bytes(sbytes):
    conv = {'B':0, 'KB':3, 'MB':6, 'GB':9, 'TB':12, 'PB':15}
    value, amount = sbytes.split(' ')
    return float(value) * (10 ** conv.get(amount, 0))


if __name__ == '__main__':
    main()