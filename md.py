#!/usr/bin/env python
#coding: utf-8

import requests
import urllib2
from bs4 import BeautifulSoup

#import urllib2
#opener = urllib2.build_opener()
#opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
#response = opener.open('http://google.com')
#htmlData = response.read()
#f = open('file.txt','w')
#f.write(htmlData )
#f.close()

#from urllib import FancyURLopener
#>>> class MyOpener(FancyURLopener):
#    ...     version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
#    ...
#    >>> myopener = MyOpener()
#    >>> myopener.retrieve('http://upload.wikimedia.org/wikipedia/en/4/44/Zindagi1976.jpg',
#            >>> 'Zindagi1976.jpg')
#    ('Zindagi1976.jpg', <httplib.HTTPMessage instance at 0x1007bfe18>)

class Comic(object):
    def __init__(self, comicUrl=""):
        self.comicUrl = comicUrl

    def download_chapter(self, chapterUrl, localPath):
        request = urllib2.Request(chapterUrl)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        print soup

        selectTag = soup.find(id="page_select")
        print selectTag
        soup.find(id="comic_page")


    def get_image(self, pageUrl, localPath):
        if self.is_url_ok:
            pageFile = open(localPath, "wb")
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageFile.write(response.read())
            pageFile.close()
            return True
        else:
            return False

        #if self.is_url_ok:
        #    pageFile = open(localPath, "wb")
        #    page = requests.get(url)
        #    pageFile.write(page.content)
        #    pageFile.close()
        #    return True
        #else:
        #    return False

    def is_url_ok(self, url):
        OK_CODE = 200
        header = requests.head(url)
        if header.status_code == OK_CODE:
            return True
        else:
            return False

def get_picture(url, lp):
    #img = urllib.urlopen(url).read()
    #img = requests.get(url)
    imgH = requests.head(url)
    print imgH.status_code
    #print(img.status_code)
    #pic = open(lp, "wb")
    #pic.write(img.content)
    #pic.close()

if __name__ == '__main__':
    url = "http://img.bato.to/comics/2015/10/24/a/read562b496b2493c/img000001.jpg"
    chUrl = "http://bato.to/reader#32ebe1a658eabee9"
    lp = "arisu1.jpg"
    #get_picture(url, lp)
    c = Comic()
    #c.get_image(url, lp)
    c.download_chapter(chUrl, lp)

