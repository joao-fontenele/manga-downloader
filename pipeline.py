#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Pipeline(object):
    def __init__(self, pipeFile='pipeline.csv'):
        self.pipe = open(pipeFile, 'r+')
        self.offset = None

    def getLine(self):
        self.offset = 1
        while True:
            try:
                self.pipe.seek(-self.offset, 2) # seek from the end of the file
            except IOError: # no more links to process
                self.offset = None
                return None
            line = self.pipe.readlines()
            if len(line) > 1:
                return line[-1]
            self.offset += 1

    def popLine(self): # removes the last line
        if not self.offset:
            return False
        self.pipe.seek(-self.offset, 2)

        # these 2 lines serve to delete the last line
        self.pipe.write('\n')
        self.pipe.truncate()

        return True

if __name__ == '__main__':
    p = Pipeline()
    print(p.getLine())
    print(p.popLine())
