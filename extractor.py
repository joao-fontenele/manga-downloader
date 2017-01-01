#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from collections import namedtuple
from BeautifulSoup import BeautifulSoup


Link = namedtuple('Link', ['addr', 'title'])

def getATag(element):
    return element.find('a')

def extractLinks(html):
    soup = BeautifulSoup(html)

    mangaName = soup.find('h1', {'class': 'ipsType_pagetitle'}).text

    chTable = soup.find('table', {'class': re.compile(r'chapters_list')})
    englishChs = chTable.findAll('tr', {'class': re.compile(r'lang_English')})
    tags = map(getATag, englishChs)
    # tags = englishChs.findAll(tag, href=re.compile(r'^https?://bato.to/reader#.*'))

    links = []
    for tag in tags:
        # tag.contents[0] is a small book logo
        link = Link(addr=str(tag.get('href')), title=str(tag.contents[1]).strip())
        links.append(link)
    return links, mangaName

def saveLinks(fname, links, mangaName):
    with open(fname, 'w') as fout:
        fout.write('#manga;addr;title\n')
        for link in links:
            fout.write('{};{};{}\n'.format(mangaName, link.addr, link.title))

def extractLinksToFile(htmlFile, fname):
    html = ''
    with open(htmlFile) as fin:
        html = fin.read()
        links, mangaName = extractLinks(html)
    saveLinks(fname, links, mangaName)

if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        usage = 'Usage: $ python {} <htmls folder>'.format(sys.argv[0])
        print(usage)
    else:
        for fname in os.listdir(path):
            htmlFile = os.path.join(path, fname)
            extension = htmlFile.split('.')[-1]
            if os.path.isfile(htmlFile) and extension == 'html':
                outFile = htmlFile.split('.')[:-1]
                outFile.append('txt')
                outFile = '.'.join(outFile)

                extractLinksToFile(htmlFile, outFile)
