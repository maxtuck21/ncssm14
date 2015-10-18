#!/usr/bin/env python

"""
Scrape etiquette: http://meta.stackexchange.com/questions/443/etiquette-of-screen-scraping-stack-overflow

 - Use GZIP requests
 - Identify yourself using the user-agent using an URL
 - Use JSON, RSS or an API when available
 - Be considerate, If pulling data for more than every 15, ask permission

"""

import os, errno
from random import randint 
from bs4 import BeautifulSoup
from urllib2 import urlopen

PROJECT = 'http://techcrunch.com/'
YEARS = range(2005, 2015)

custom_headers = {'content-encoding': 'gzip', 
                  'User-Agent': 'WikiBrowser/1.0 Gecko/1.0',
                  'From': 'irwin2014@gmail.com'}

def get_url(url, year):
    urls = []
    for i in range(1, 643):
        urls.append(url + year + "/page/" + str(i))
    return urls

def get_list_of_urls(project):
    """
    Return a list of urls based on the post title.
    """
    soup = get_content(project)
    li = soup.find_all('h2', class_='post-title')
    urls = [link.find('a').get('href') for link in li]
    return urls

def get_content(url):
   return BeautifulSoup(requests.get(url).text, headers=custom_headers)
   # return soup.find('div', class_='article-entry').find_all('p')

def main():
    # article = get_content(URL)
    # print (' ').join([p.string for p in article])
    print(get_years_available(PROJECT, '2006'))

# big method that handles IO and combines all filters and such
def collect(urls, year):
    try:
        os.remove('test.txt')
    except OSError:
        pass
    
    file = open('test.txt', 'w+')
    file.close()

    articles = []
    # get the specific links
    n = 0
    for url in urls:
        url = urlopen(url)
        n += 1
        print(n)
        # open up the file and use Beautiful Soup
        soup = BeautifulSoup(url, "html.parser")
        for link in soup.find_all('a'):
            articles.append(link.get('href'))
    with open('test.txt', 'r+w+') as file:
        # apply filters to filter URLs
        articles = clean_links(articles, year)
#        articles = remove_every_other(articles)
        

        # write the resulting URLs to file
        for link in articles:
            file.write(link.encode('utf-8') + "\n")

# filter all the stuff
def clean_links(links, year):
    articles = []
    for link in links:
        # do not want comments, but want techcrunch.com to prevent ads
        if "#comment" not in link.encode('utf-8'):
            articles.append(link.encode('utf-8'))
    return articles

# skip every 2, since there are repeats
def remove_every_other(links):
    return links[::2]


if __name__ == '__main__':
#    main()
    
    collect(get_url(PROJECT, '2009'), '2009')


