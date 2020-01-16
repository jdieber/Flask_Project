from bs4 import BeautifulSoup as bs
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
import os
import sys
import requests
import urllib.request 

url = 'https://cheezburger.com/2160645/21-funniest-memes-of-the-day'
r = requests.get(url)
html = r.text
soup = bs(html, 'lxml')

data = soup.find_all("div", {"class": "resp-media-wrap"})

links = []
for a in soup.find_all("div", {"class": "resp-media-wrap"}):
    if a.img:
        links.append(a.img['data-src'])

meme = links[0]