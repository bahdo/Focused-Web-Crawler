#Gabriel Akdemir
#IS 392 2018S Section 002
#Focused Web Crawler Assignment


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os


#gets page content
def get_page_content(url):
	try:
		html_response_text = urlopen(url).read()
		page_content = html_response_text.decode('utf-8')
		return page_content
	except Exception as e:
		return None

#saves page
def save(text, path):
	f = open(path, 'w', encoding = 'utf-8', errors = 'ignore')
	f.write(text)
	f.close()

#extracts outgoing Urls from page content
def get_urls(soup):
	links = soup.find_all('a')
	urls = []
	for link in links:
		urls.append(link.get('href'))
	return urls
    
#checks if a URL is valid
def is_url_valid(url):
	if url is None:
		return False
	if re.search('#', url):
		return False
	match = re.search('^/wiki/',url)
	if match:
		return True
	else:
		return False
	    
#reformats URL into a full URL
def reformat_url(url):
	match=re.search('^/wiki/',url)
	if match:
		return "https://en.wikipedia.org"+url
	else:
		return url

#cleans title
def clean_title(title):
	invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
	for c in invalid_characters:
		title = title.replace(c,'')
	return title


#setup SSL environment
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#Seed URL is searched for terms specified in the list relatedTerms
seedUrls = ["http://en.wikipedia.org/wiki/Msuic","http://en.wikipedia.org/wiki/Sound"]
relatedTerms = ["hip-hop","rap","rock","Michael Jackson", "Kanye West", "pop", "drum", "piano", "tambourine", "sound", "singing", "stage", "microphone",
				"booth", "Quincy Jones", "chanting", "metal", "synthesizer", "instrument", "MTV", "music", "entertainment", "rythm", "symphony",
				"Orchestra", "pitch", "timbre", "flute"]


visitedUrlList = []
queue = []
pageCounter = 0
savedUrlList = []

#for loop loops through URLs and puts it in the Queue and list of visited URLs
for url in seedUrls:
    queue.append(url)
    visitedUrlList.append(url)
    
while queue: #while the queue is not empty pop queue and get content of the webpage
    url = queue.pop(0)
    pageContent = get_page_content(url)
    soup = BeautifulSoup(pageContent,'html.parser')
    pageMainText = soup.get_text()
    
    termCounter = 0
    for term in relatedTerms: #checks for terms in the page if it occurs 2 or more times it's topical relevant
        if re.search(term, pageMainText, re.I):
            termCounter = termCounter+1
            if termCounter >= 2:#cleans the title and saves
                pageTitle = soup.title.string
                pageTitle = clean_title(pageTitle)
                save(pageTitle, "/Users/gabrielakdemir/Documents/visitedUrls.txt")
                savedUrlList.append(url)
                pageCounter = pageCounter+1
                print("Page #"+str(pageCounter)+": "+url)
                break
    if pageCounter >= 500: #once it crawls 500 pages it breaks out of the loop
        break
    outGoingUrls = get_urls(soup)
    for outGoingUrl in outGoingUrls: #adds all of the valid URLs to the queue and visitedURLlist
        if is_url_valid(outGoingUrl):
            outGoingUrl = reformat_url(outGoingUrl)
            if outGoingUrl not in savedUrlList:
                queue.append(outGoingUrl)
                visitedUrlList.append(outGoingUrl)
            
#writes to the txt file all the pages crawled
f= open("visitedUrls.txt","w")
i = 1
for url in savedUrlList:
    f.write(str(i) + ': ' + url + '\n')
    i+=1
f.close()