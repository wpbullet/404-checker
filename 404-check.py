#!/usr/bin/env python2.7
# Author Mike https://guides.wp-bullet.com/
# Forked from https://gist.github.com/chrisguitarguy/1305010
from argparse import ArgumentParser
import csv
from itertools import izip
import requests
from BeautifulSoup import BeautifulStoneSoup as Soup

#url="https://guides.wp-bullet.com/post-sitemap.xml"


#create empty lists
#itemstowrite = []
#itemsresponsecode = []
#print itemstowrite
#print urls

#loop through all urls of sitemap
def parse_sitemap(url):
    resp = requests.get(url)
    soup = Soup(resp.content)
    responsecode = resp.status_code
    urls = soup.findAll('url')
#    itemsparent=[]
#    itemstowrite = []
#    itemsresponsecode = []
    for url in urls:
    #create empty lists
        itemsparent=[]
        itemstowrite = []
        itemsresponsecode = []
        loc = url.find('loc').string
        print loc
        depthrequest = requests.get(loc)
        depthsoup = Soup(depthrequest.content)
        #print depthsoup
        imagesall = depthsoup.findAll('img', src=True)
#       imagessrc=imagesall.findall('src')
#       print imagesall
        for image in imagesall:
            imageprocess = image['src']
            print imageprocess
            respimage = requests.get(imageprocess)
            respimagecode = respimage.status_code
            print respimagecode
            #itemsparent.append(loc)
            itemstowrite.append(imageprocess)
            itemsresponsecode.append(respimagecode)
        print itemstowrite
        print itemsresponsecode
        itemsparent.append(loc)
#    return itemstowrite, itemsresponsecode, itemsparent
        with open(args.out, 'a') as f:
             writer = csv.writer(f)
             writer.writerows(zip(itemsparent))
             writer.writerows(izip(itemstowrite, itemsresponsecode))

 if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store', dest='url', help='The file contain one url per line')
    options.add_argument('-o', '--output', action='store', dest='out', default='results.csv', help='Where you would like to save the data')
    args = options.parse_args()
    urls = parse_sitemap(args.url)
    if not urls:
        print 'There was an error!'
