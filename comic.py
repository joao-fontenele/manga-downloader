#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import sys
import time
from math import log
from math import ceil
from ConfigParser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Comic(object):
    def __init__(self, folder, logger, configPath='config.cfg', pageLoadTimeout=90):
        self.folder = folder
        self.driver = None
        self.pageLoadTimeout = pageLoadTimeout
        self.logger = logger

        config = ConfigParser()
        if config.read(configPath):
            self.user = config.get('User Login', 'user')
            self.pw = config.get('User Login', 'pw')
        else:
             self.setupConfig(configPath)

    def setupConfig(self, configPath):
        self.user = raw_input('username: ')
        self.pw = raw_input('password: ')

        config = ConfigParser()
        config.add_section('User Login')

        config.set('User Login', 'user', self.user)
        config.set('User Login', 'pw', self.pw)

        config.write(open(configPath, 'w'))

    def locateElement(self, cssSelector, waitTime=3):
        wait = WebDriverWait(self.driver, waitTime)
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector)))

    def login(self, loginUrl='https://bato.to/forums/index.php?app=core&module=global&section=login'):
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.implicitly_wait(0)
        driver.set_page_load_timeout(self.pageLoadTimeout)
        self.loadPage(loginUrl)

        userInput = self.locateElement('#ips_username')
        passInput = self.locateElement('#ips_password')
        userInput.send_keys(self.user)
        passInput.send_keys(self.pw)
        passInput.submit()

    def close(self):
        self.driver.quit()

    def getChapterName(self):
        driver = self.driver
        chapterSelect = self.locateElement('select[name=chapter_select]')
        selected = self.locateElement('option[selected]')

        comicName = self.locateElement('div.moderation_bar > ul > li > a').text
        chapterName = comicName + ' - ' + selected.text

        return chapterName

    def getAllPagesUrls(self, selectId='page_select'):
        driver = self.driver

        pageSelect = self.locateElement('#' + selectId)
        opts = pageSelect.find_elements_by_tag_name('option')

        links = []
        for opt in opts:
            links.append(opt.get_attribute('value'))
        return links

    def getImageUrlFromPageUrl(self, pageUrl=None, retriesLeft=2):
        driver = self.driver
        if pageUrl:
            try:
                self.loadPage(pageUrl)
            except TimeoutException:
                self.logger.log('timeout on page load')
                pass

        img = self.locateElement('#comic_page')

        return img.get_attribute('src')

    def downloadImage(self, url, path, fileName, chunkSize=1024):
        resp = requests.get(url)

        if resp.status_code == 200:
            with open(path + fileName, 'wb') as fd:
                for chunk in resp.iter_content(1024):
                    fd.write(chunk)
        return resp.status_code

    def fancyDownloadImage(self, url, path, fileName, chunkSize=1024):
        status = self.downloadImage(url, path, fileName, chunkSize)
        extension = url.split('/')[-1].split('.')[-1]
        if status != 404 or extension not in ['jpg', 'png']:
            return status

        ivertedExtension = 'png' if extension == 'jpg' else 'jpg'
        url = url[:-3] + ivertedExtension
        fileName = fileName[:-3] + ivertedExtension

        return self.downloadImage(url, path, fileName, chunkSize)

    def getImagePath(self, folder, chapterName, imgUrl):
        fileName = imgUrl.split('/')[-1]
        return (folder + chapterName + '/', fileName)

    def loadPage(self, url):
        driver = self.driver
        try:
            self.logger.log('loading {}'.format(url))
            driver.get(url)
        except TimeoutException:
            self.logger.log('normal timeout on page loading {}'.format(url))

    def getOptmisticImgUrls(self, exampleImgUrl, pages):
        split = exampleImgUrl.split('/')
        fileName, extension = split[-1].split('.')
        baseUrl = '/'.join(split[:-1]) + '/'

        digits = int(ceil(log(pages + 1, 10)))

        formatStr = '{}{:0' + str(digits) + 'd}.{}'

        imgs = []
        for i in range(pages):
            newFile = formatStr.format(fileName[:-digits], i + 1, extension)
            imgs.append(baseUrl + newFile)

        return imgs

    def getImgUrlNormally(self, pageUrl, seen, retries=20):
        imgUrl = self.getImageUrlFromPageUrl(pageUrl)

        for i in range(retries):
            if seen.get(imgUrl, False):
                time.sleep(1)
                imgUrl = self.getImageUrlFromPageUrl()
            else:
                break

        if seen.get(imgUrl, False):
            raise Exception('Could not get a new img url from {} after {} retries. Seen urls={}'.format(pageUrl, retries, seen))

        return imgUrl

    def downloadChapter(self, firstPageUrl, retries=20):
        if not self.driver:
            self.login()

        driver = self.driver
        self.loadPage(firstPageUrl)

        time.sleep(10) # DOM may still be with the last url contents

        # retry once
        chapterName = None
        try:
            chapterName = self.getChapterName()
        except TimeoutException:
            self.loadPage(firstPageUrl)
            chapterName = self.getChapterName()
        pagesUrls = self.getAllPagesUrls()
        imgUrl = self.getImageUrlFromPageUrl()
        chapterName = chapterName.replace(':', '')

        # creating folders if it doesn't exist
        path, fileName = self.getImagePath(self.folder, chapterName, imgUrl)
        if not os.path.exists(path):
            os.makedirs(path)

        imgsUrls = self.getOptmisticImgUrls(imgUrl, len(pagesUrls))

        errors = []
        seen = dict()
        self.logger.log('downloading chapter: {}'.format(chapterName.encode('ascii', 'ignore')))
        self.logger.log('  found {} pages'.format(len(pagesUrls)))

        for i, imgUrl in enumerate(imgsUrls):
            self.logger.log('    optimistic url -> {}'.format(imgUrl))
            path, fileName = self.getImagePath(self.folder, chapterName, imgUrl)
            status = self.fancyDownloadImage(imgUrl, path, fileName)
            seen[imgUrl] = True

            if status != 200:
                imgUrl = self.getImgUrlNormally(pagesUrls[i], seen)
                seen[imgUrl] = True
                self.logger.log('    optimistic failed! loading from page {} -> {}'.format(pagesUrls[i], imgUrl))
                path, fileName = self.getImagePath(self.folder, chapterName, imgUrl)
                status = self.fancyDownloadImage(imgUrl, path, fileName)
                if status != 200:
                    errors.append(imgUrl)
                    self.logger.log('    status_code for url: {} is {}'.format(imgUrl, status))

        if errors:
            self.logger.log('  there were some errors in the following urls')
            for e in errors:
                self.logger.log('    {}'.format(e))


def test():
    c = Comic('')
    url = 'http://img.bato.to/comics/2016/05/19/s/read573d700431726/img000001.jpg'

    imgs = c.getOptmisticImgUrls(url, 100)
    for img in imgs:
        print img

if __name__ == '__main__':
    folder = 'Downloads/'
    # test()

    if len(sys.argv) > 1:
        c = Comic(folder=folder)
        urls = sys.argv[1:]
        for url in urls:
            c.downloadChapter(firstPageUrl=url)
        c.close()
    else:
        print('give me a list of whitespace separated comic urls')
