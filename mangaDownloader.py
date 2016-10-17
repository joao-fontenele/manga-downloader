#!/usr/bin/env python
# coding: utf-8

import requests
import time
from selenium import webdriver
import os
import sys
from math import log
from math import ceil
import time


class Comic(object):
    def __init__(self, folder):
        self.folder = folder
        self.driver = None

    def login(self, loginUrl='https://bato.to/forums/index.php?app=core&module=global&section=login', user='jp_shiro', pw='IUNiuQGHq3soWXGXwQNn'):
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.implicitly_wait(3)
        driver.get(loginUrl)

        userInput = driver.find_element_by_id('ips_username')
        passInput = driver.find_element_by_id('ips_password')
        userInput.send_keys(user)
        passInput.send_keys(pw)
        passInput.submit()

    def close(self):
        self.driver.quit()

    def getChapterName(self):
        driver = self.driver
        chapterSelect = driver.find_element_by_name('chapter_select')
        selected = chapterSelect.find_element_by_css_selector('option[selected]')

        comicName = driver.find_element_by_css_selector('div.moderation_bar > ul > li > a').text
        chapterName = comicName + ' - ' + selected.text

        return chapterName

    def getAllPagesUrls(self, selectId='page_select'):
        driver = self.driver

        pageSelect = driver.find_element_by_id(selectId)
        opts = pageSelect.find_elements_by_tag_name('option')

        links = []
        for opt in opts:
            links.append(opt.get_attribute('value'))
        return links

    def getImageUrlFromPageUrl(self, pageUrl=None):
        driver = self.driver
        if pageUrl:
            driver.get(pageUrl)

        img = driver.find_element_by_id('comic_page')
        return img.get_attribute('src')

    def downloadImage(self, url, path, fileName, chunkSize=1024):
        resp = requests.get(url)

        if resp.status_code == 200:
            with open(path + fileName, 'wb') as fd:
                for chunk in resp.iter_content(1024):
                    fd.write(chunk)
        return resp.status_code

    def getImagePath(self, folder, chapterName, imgUrl):
        fileName = imgUrl.split('/')[-1]
        return (folder + chapterName + '/', fileName)

    def downloadChapter(self, firstPageUrl, retries=20):
        if not self.driver:
            self.login()

        driver = self.driver
        driver.get(firstPageUrl)

        chapterName = self.getChapterName()
        pagesUrls = self.getAllPagesUrls()
        imgUrl = self.getImageUrlFromPageUrl()

        # creating folders if it doesn't exist
        path, fileName = self.getImagePath(self.folder, chapterName, imgUrl)
        if not os.path.exists(path):
            os.makedirs(path)

        errors = []
        seen = dict()
        print('downloading chapter: {}'.format(chapterName))
        print('  found {} pages'.format(len(pagesUrls)))

        for url in pagesUrls:
            imgUrl = self.getImageUrlFromPageUrl(url)
            for i in range(retries):
                if seen.get(imgUrl, False):
                    time.sleep(1)
                    imgUrl = self.getImageUrlFromPageUrl()
                else:
                    seen[imgUrl] = True
                    print('  NEW url'),
                    break
            print('from page {} -> {}'.format(url, imgUrl))
            path, fileName = self.getImagePath(self.folder, chapterName, imgUrl)
            status = self.downloadImage(imgUrl, path, fileName)
            if status != 200:
                errors.append(imgUrl)
                print('    status_code for url: {} is {}'.format(imgUrl, status))

        if errors:
            print('  there were some errors in the following urls')
            for e in errors:
                print('    {}'.format(e))


if __name__ == '__main__':
    folder = 'Downloads/'

    if len(sys.argv) > 1:
        c = Comic(folder=folder)
        urls = sys.argv[1:]
        for url in urls:
            time.sleep(3)
            c.downloadChapter(firstPageUrl=url)
        c.close()
    else:
        print('give me a list of whitespace separated comic urls')
