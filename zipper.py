#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from zipfile import ZipFile

def compress(mangaFolder, archivePath):
    mangaTitle = mangaFolder.split(os.path.sep)[-1] # TODO more generic way?
    archive = os.path.join(archivePath, mangaTitle)
    archive = os.path.abspath(archive)
    mangaPath = os.path.abspath(mangaFolder)
    currDir = os.getcwd()
    os.chdir(mangaFolder)
    with ZipFile(archive + '.zip', 'w') as manga:
        for fname in os.listdir(mangaPath):
            manga.write(fname)
    os.chdir(currDir)

if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        usage = 'Usage: $ python {} <mangas folder>'.format(sys.argv[0])
        print(usage)
    else:
        for folder in os.listdir(path):
            if os.path.isdir(os.path.join(path, folder)):
                compress(os.path.join(path, folder), path)
