#!/usr/bin/env python
# coding: utf-8

import requests

class Comic(object):
    def __init__(self, folder, comicName, comicUrl):
        self.folder = folder
        self.comicName = comicName
        self.comicUrl = comicUrl

    def getPage(self, url, path, chunkSize=1024):
        resp = requests.get(url)
        with open(path, 'wb') as fd:
            for chunk in resp.iter_content(1024):
                fd.write(chunk)

if __name__ == '__main__':
    folder = 'saikin'
    comicUrl = 'http://bato.to/reader#196b28aa4a4d3640'
    comicPageUrl = 'http://img.bato.to/comics/2015/10/28/s/read56307d3cc9e21/img000042.jpg'
    comicName = 'saikin'

    c = Comic(folder, comicName, comicUrl)
    path = folder + '/' + comicPageUrl.split('/')[-1]
    print('saving to {}'.format(path))
    c.getPage(comicPageUrl, path)
