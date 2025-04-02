# sources:
# https://www.c-sharpcorner.com/article/extract-e-mail-id-from-a-webpage/
# https://www.geeksforgeeks.org/deque-in-python/
# https://stackoverflow.com/questions/25471450/python-getting-all-links-from-a-google-search-result-page
# https://stackoverflow.com/questions/17153779/how-can-i-print-variable-and-string-on-same-line-in-python

#import packages
import os
from bs4 import BeautifulSoup  
import requests  
import requests.exceptions  
from urllib.parse import urlsplit  
from collections import deque  
import re
from googlesearch import search


#-------------------------------------------------------------------------------------
# set variables for site searcher
# set the number of Google Search results to process
num_results = 10


#-------------------------------------------------------------------------------------
# set variables for site crawler
# a queue of urls to be crawled  
#new_urls = deque(['http://www.theprotolab.com/contact-us/','https://www.bv.com/contact-us'])
new_urls = deque()
# a set of urls that we have already crawled  
processed_urls = set()
# a set of crawled emails  
emails = set()


#-------------------------------------------------------------------------------------
# site searcher
# prompt the user to enter a search query
query = input('Please type the company or keyword you would like to search: ')
num_results = int(input('How many websites would you like to search? '))

print("Here are the following Google results for", query, ":")
# gather the list of search results
for result in search(query, tld="co.in", num=num_results, stop=num_results, pause=2):
    new_urls.append(result)
# print the list of search results
for url in new_urls:
    print(url)


#-------------------------------------------------------------------------------------
# site crawler
# process urls one by one until we exhaust the queue  
print("\n")
while len(new_urls):  
    # move next url from the queue to the set of processed urls  
    url = new_urls.popleft()
    processed_urls.add(url)  
    # get url's content  
    print("Processing %s" % url)  
    try:  
        response = requests.get(url)  
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):  
        # ignore pages with errors   
        continue

    # extract base url and path to resolve relative links  
    parts = urlsplit(url)  
    base_url = "{0.scheme}://{0.netloc}".format(parts)  
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # extract all email addresses and add them into the resulting set   
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))  
    emails.update(new_emails)

    # create a beutiful soup for the html document  
    soup = BeautifulSoup(response.text, "html.parser")

#    # find and process all the anchors in the document  
#    for anchor in soup.find_all("a"):  
#        # extract link url from the anchor  
#        link = anchor.attrs["href"] if "href" in anchor.attrs else ''  
#        # resolve relative links  
#        if link.startswith('/'):  
#            link = base_url + link  
#        elif not link.startswith('http'):  
#            link = path + link  
#        # add the new url to the queue if it was not enqueued nor processed yet  
#        if not link in new_urls and not link in processed_urls:  
#            new_urls.append(link)


#-------------------------------------------------------------------------------------
# print the resulting emails
print("\nEmail addresses for", query, ":")
for email in emails:
    if not ("png" or "jpg" or "yourname") in email:
        print(email)

os.system("pause")
os._exit(0)
