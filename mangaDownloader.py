#!/usr/bin/env python
# coding: utf-8

import requests
import time
from selenium import webdriver
import os
import sys


class Comic(object):
    def __init__(self, folder):
        self.folder = folder
        self.login()

    def login(self, loginUrl='https://bato.to/forums/index.php?app=core&module=global&section=login', user='jp_shiro', pw='IUNiuQGHq3soWXGXwQNn'):
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(loginUrl)

        userInput = driver.find_element_by_id('ips_username')
        passInput = driver.find_element_by_id('ips_password')
        userInput.send_keys(user)
        passInput.send_keys(pw)
        passInput.submit()

    def getChapterName(self):
        driver = self.driver
        chapterSelect = driver.find_element_by_name('chapter_select')
        selected = chapterSelect.find_element_by_css_selector('option[selected]')

        comicName = driver.find_element_by_css_selector('div.moderation_bar > ul > li > a').text
        chapterName = comicName + ' - ' + selected.text

        return chapterName

    def getAllPagesUrls(self, firstPageUrl, selectId='page_select'):
        driver = self.driver

        pageSelect = driver.find_element_by_id(selectId)
        opts = pageSelect.find_elements_by_tag_name('option')

        links = []
        for opt in opts:
            links.append(opt.get_attribute('value'))
        return links

    def getImageUrlFromPageUrl(self, pageUrl):
        driver = self.driver
        driver.get(pageUrl)
        img = driver.find_element_by_id('comic_page')
        return img.get_attribute('src')

    def downloadImage(self, url, path, fileName, chunkSize=1024):
        resp = requests.get(url)

        if not os.path.exists(path):
            os.makedirs(path)

        print('downloading file: {}'.format(fileName))
        with open(path + fileName, 'wb') as fd:
            for chunk in resp.iter_content(1024):
                fd.write(chunk)

    def getImagePath(self, folder, chapterName, imgUrl):
        fileName = imgUrl.split('/')[-1]
        return (folder + '/' + chapterName + '/', fileName)

    def downloadChapter(self, firstPageUrl):
        driver = self.driver
        driver.get(firstPageUrl)
        chapterName = self.getChapterName()
        pagesUrls = self.getAllPagesUrls(firstPageUrl)

        print('downloading chapter: {}'.format(chapterName))
        for url in pagesUrls:
            imgUrl = self.getImageUrlFromPageUrl(url)
            path, fileName = self.getImagePath(self.folder, chapterName, imgUrl)
            self.downloadImage(imgUrl, path, fileName)
        print('finished downloading chapter: {}\n'.format(chapterName))

if __name__ == '__main__':
    folder = 'Downloads/manga/'

    if len(sys.argv) > 1:
        c = Comic(folder=folder)
        urls = sys.argv[1:]
        for url in urls:
            c.downloadChapter(firstPageUrl=url)
    else:
        print('give me a list of whitespace separated comic urls')
