#!/usr/bin/env python
# coding: utf-8

import re
from collections import namedtuple
from BeautifulSoup import BeautifulSoup


Link = namedtuple('Link', ['addr', 'title'])

def getATag(element):
    return element.find('a')

def extractLinks(html):
    soup = BeautifulSoup(html)

    chTable = soup.find('table', {'class': re.compile(r'chapters_list')})
    englishChs = chTable.findAll('tr', {'class': re.compile(r'lang_English')})
    tags = map(getATag, englishChs)
    # tags = englishChs.findAll(tag, href=re.compile(r'^https?://bato.to/reader#.*'))

    links = []
    for tag in tags:
        # tag.contents[0] is a small book logo
        link = Link(addr=str(tag.get('href')), title=str(tag.contents[1]).strip())
        links.append(link)
    return links

def saveLinks(fname, links):
    with open(fname, 'w') as fout:
        fout.write('#addr;title\n')
        for link in links:
            # print link
            fout.write('{};{}\n'.format(link.addr, link.title))

def extractLinksToFile(html, fname):
    saveLinks(fname, extractLinks(html))

if __name__ == '__main__':
    html = open('examples/ps.html').read()
    extractLinksToFile(html, 'examples/ps.csv')
