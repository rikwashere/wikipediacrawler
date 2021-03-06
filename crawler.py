# -*- coding: utf-8 -*-

import os
import re
import json
import random
import requests
import datetime
from bs4 import BeautifulSoup

def linkValidator(url, urls):
	if url != None:
			if url in urls.keys():
				return False
			if re.findall(':', url):
				return False
			if len(url.split('/')) < 2:
				return False
			if url.split('/')[1] == 'wiki':
				return True
	else:
		return False

def getCategories(soup):
	strainer = soup.find( 'div', {'id' : 'mw-normal-catlinks'})
	if strainer:
		cats = strainer.select('li')
		return [cat.string for cat in cats]

def getRevHistory(soup):
	link = soup.find('a', {'accesskey' : 'h'})
	rev_history_url = root + link.get('href')
	url = rev_history_url.split('&')[0] + '&offset=&limit=1000' + '&' + rev_history_url.split('&')[1]
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	ts = []
	for timestamp in soup.find_all('a', {'class' : 'mw-changeslist-date'}):
		ts.append(timestamp.string)
	return ts


def getLinks(page, urls):
	r = requests.get(page)
	soup = BeautifulSoup(r.text, "html.parser")
	validated = 0
	for link in soup.find_all('a'):
		url = link.get('href')
		if linkValidator(url, urls):
			entry = { root + url : { 'categories' : None, 'revision_history' : None, 'title' : None} }
			urls.update(entry)
			validated += 1
	print '\t+ Found %i valid urls on "%s".' % (validated, page)
	return urls

def getComment(soup):
	revisions = soup.find_all('span', { 'class' : 'comment'})
	print revisions
	return None
		
if __name__ == '__main__':
	num_pages = 1000
	root = 'https://en.wikipedia.org'
	start_url = '/wiki/Main_page'
	print '\nCrawling Wikipedia. Looking for %i urls.' % num_pages
	urls = {}
	while len(urls) < num_pages:
		if len(urls) == 0:
			page = root + start_url
			print '* Starting at "%s."' % page
		else:
			page = random.choice(urls.keys())
		print 'Crawling further from "%s".' % page
		getLinks(page, urls)
		print '* Currently crawled %s urls.' % len(urls.keys())
	print 'Crawled %i hyperlinks.' % len(urls.keys())

	first_x = urls.keys()[:num_pages]
	print '\nGathering and storing data...'

	if os.path.isfile('wikipedia.json'):
		print 'Output file already exists. Overwrite?'
		#ans = raw_input('Y/N')
		#if ans.lower == 'y':
		os.remove('wikipedia.json')
	else:
		print 'Saving to "wikipedia.json".'

	for num, page in enumerate(first_x):
		print '* Populating "%s".' % page
		data = urls[page]
		r = requests.get(page)
		soup = BeautifulSoup(r.text, "html.parser")
		data['categories'] = getCategories(soup)
		data['title'] = soup.title.string.split('-')[0]
		data['revision_history'] = (getRevHistory(soup), getComment(soup))
		with open('wikipedia.json', 'a') as json_out:
			json.dump(urls[page], json_out)
			json_out.write('\n')
		print 'Populated %i/%i urls.' % (num, len(first_x))	