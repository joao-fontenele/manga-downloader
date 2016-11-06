#!/usr/bin/env python
# coding: utf-8

from comic import Comic
from pipeline import Pipeline
import argparse
import time
import traceback


def createParser():
    description = """
        This is a manga downloader tool, used and developed by JP, to download
        manga from bato.to"""
    parser = argparse.ArgumentParser(description=description)
    chapterHelp = """
        chapter is a url to the single chapter to be downloaded
        """
    pipelineHelp = """
        pipeline is the path to a file with the links to chapters you want to
        download
        """
    downloadHelp = '''
        download is the path to the folder where you want the chapters to
        be saved to
        '''

    parser.add_argument('-ch', '--chapter', help=chapterHelp, dest='chUrl')
    parser.add_argument('-dl', '--download', help=downloadHelp, dest="folder",
            default='Downloads/')
    parser.add_argument('-pp', '--pipeline', help=pipelineHelp, dest="pipeFile",
            default='pipeline.txt')

    return parser

def downloadChapter(comic, url, title=None, retries=5):
    prettyChName = '({}) {}'.format(title if title else 'untitled', url)

    count = 1
    while count <= retries:
        try:
            comic.downloadChapter(firstPageUrl=url)
        except Exception as e:
            traceback.print_exc()
            print('retrying {}/{}, for {}'.format(count, retries, prettyChName))
            count += 1
        else:
            break
    else:
        raise Exception('Failed to download chapter ' + prettyChName)

def main():
    parser = createParser()
    args = parser.parse_args()

    print('saving to folder: {}\n'.format(args.folder))
    comic = Comic(args.folder)

    if args.chUrl:
        downloadChapter(comic, args.chUrl)
    else:
        pipe = Pipeline(args.pipeFile)

        line = pipe.getLine()
        while line:
            url, title = line.split(';')
            title = title.strip()
            downloadChapter(comic=comic, url=url, title=title)
            print('done downloading this chapter\n')
            pipe.popLine()
            line = pipe.getLine()

    print('\nno more work to do\n')

    c.close()

if __name__ == '__main__':
    main()
