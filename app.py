#!/usr/bin/env python

"""
Scrape etiquette: http://meta.stackexchange.com/questions/443/etiquette-of-screen-scraping-stack-overflow

 - Use GZIP requests
 - Identify yourself using the user-agent using an URL
 - Use JSON, RSS or an API when available
 - Be considerate, If pulling data for more than every 15, ask permission

"""

import os, errno
import csv
import time
import requests
from random import randint 
from bs4 import BeautifulSoup
from urllib2 import urlopen


PROJECT = 'http://techcrunch.com/'
YEARS = range(2005, 2015)

custom_headers = {'content-encoding': 'gzip', 
                  'User-Agent': 'WikiBrowser/1.0 Gecko/1.0',
                  'From': 'irwin2014@gmail.com'}

def get_years_available(url, year):
    """
    Test how many pages are available in a year
    """
    results = []
    def populate_results(count):
        """
        This will send a GET request to the url and check if is successful,
        it will append the url to the results list until it get a 404.
        """

        # ex: `http://techcrunch.com/2005/page/2`
        new_url = url + str(year) + '/page/' + str(count)
        r = requests.get(new_url, headers=custom_headers)
        if r.status_code == 200:
            results.append(new_url)

            # We add some sleep time to don't get mad the webmaster :) also
            # we set a variable number between 0 and 5 seconds for look less
            # like a bot.
            time.sleep(randint(0, 5))
            populate_results(count + 1)
        else:
            pass 

    populate_results(2)
    return results

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
    print(get_years_available(PROJECT, '2005'))

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
    for url in urls:
        url = urlopen(url)
        # open up the file and use Beautiful Soup
        soup = BeautifulSoup(url, "html.parser")
        for link in soup.find_all('a'):
            articles.append(link.get('href'))
    with open('test.txt', 'r+w+') as file:
        # apply filters to filter URLs
        articles = clean_links(articles, year)
        articles = remove_every_other(articles)
        

        # write the resulting URLs to file
        for link in articles:
            file.write(str(link) + "\n")

# filter all the stuff
def clean_links(links, year):
    articles = []
    for link in links:
        # do not want comments, but want techcrunch.com to prevent ads
        if ( "#comment" not in str(link) and
                "http://techcrunch.com/" + str(year) in str(links) ):
            articles.append(str(link))
    return articles

# skip every 2, since there are repeats
def remove_every_other(links):
    return links[::2]


if __name__ == '__main__':
#    main()
    
    collect(get_years_available(PROJECT, '2005'), '2005')


