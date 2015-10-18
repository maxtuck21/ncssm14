# coding: utf-8
#import urllib2
import urllib
import sys
import base64
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


def search_company(company, links):
	company_articles = []
	for link in links:
		if company in link:
			company_articles.append(link)
	return company_articles


def sentiment(input):
	account_key = 'et0av6RSWeINmtWlaz1RYJSEE2DwNepfDh/H8wRxDv0='
	base_url = 'https://api.datamarket.azure.com/data.ashx/amla/text-analytics/v1'
	creds = base64.b64encode('AccountKey:' + account_key)
	headers={'Content-Type':'application/json', 'Authorization':('Basic '+ creds)}


	params = { 'Text': input}
	# sentiment
	sentiment_url = base_url + '/GetSentiment?' + urllib.urlencode(params)
	req = urllib2.Request(sentiment_url, None, headers)
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)
	return str(obj['Score'])

def transform(links):
	a=[None]*len(links)
	for x in range(0,len(links)):
		html=urlopen(links[x])
		soup = BeautifulSoup(html, "html.parser")
		soupText=str(soup.find_all('p'))
		try: 
			a[x]=sentiment(soupText)
		except urllib2.HTTPError:
			x += 1
		x += 1
	return a
	
		
		
	

def main():
	COMPANY = "google"
	with open('url2005.txt', 'r+') as file:
		links = file.read().splitlines()
	content=(search_company(COMPANY, links))
	print(content)
	#with open("url2005.txt") as f:
	#	content=f.read().splitlines()
	#print(content)
	print(transform(content))
	
	

main()
