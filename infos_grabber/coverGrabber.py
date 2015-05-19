#!/usr/bin/python

import requests
from bs4 import BeautifulSoup


class CoverGrabber:
    def __init__(self, url=None):
        if not url:
            self.url = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias=aps&field-keywords=book'
        else:
            self.url = url

    def request_service(self, keyword):
        complete_url = "%s %s" % (self.url, keyword)
        html = requests.get(complete_url)
        soup = BeautifulSoup(html.text)
        return soup

    def grab(self, keyword):
        try:
            soup = self.request_service(keyword)
            image = soup.find_all("img",
                                  {"class": "s-access-image"})[0].get('src')
            return image
        except:
            return None


if __name__ == "__main__":
    print "Grab Book Cover from Amazon"
    cover_grabber = CoverGrabber()

    cover = cover_grabber.grab('Harry Potter')
    if not cover:
        print "Error"
    else:
        print "Cover : %s" % cover
