#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Logger(object):
    def __init__(self, logPath='log.txt'):
        self.fout = open(logPath, 'r+')

    def log(self, message):
        print(message)
        self.fout.write(message)
        self.fout.write('\n')

    def close(self):
        self.fout.close()
        self.fout.flush()
