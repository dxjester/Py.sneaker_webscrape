# -*- coding: utf-8 -*-
"""
FILENAME: sneakernews_scrape.py
PROJECT: Sneaker Website Analysis
DATE CREATED: 15-Aug-19
DATE UPDATED: 16-AUG-19
VERSION: 1.0
"""



#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 1: Import Libraries ------------------------#
#-----------------------------------------------------------------------------#

# 1.1 Module Import ----------------------------------------------------------#
# import the required modules
import nltk 
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation


# retrieve the url 
url = 'https://sneakernews.com/'
r = requests.get(url)
type(r)

# utilize Beautiful soup to read in 
soup = BeautifulSoup(r.content, "html.parser")
type(soup)

soup.title

# retrieve all hyperlinks within the webpage and store as a list
hyperlink_list = soup.findAll('a')
hyperlink_list

# find all paragraphs in the webpage
hyperlink_list = soup.findAll('p')
hyperlink_list

# convert the ingest as a text
sneaker_text = soup.get_text()
print(sneaker_text)

lines = [sneaker_text.lower() for line in sneaker_text]
lines


nike_list = ['Nike', 'Air', 'Max', 'Jordan', 'Zoom', 'React', 'Shox', 'ACG', 'Max Plus', 'Joyride', 'Tinker', 'Force', 'Westbrook', 'Kyrie','Lebron', 'Durant', 'SB', 'Air Max 90', 'Air Max 1', 'Kyrie', 'Air Max 270', 'Travis Scott' ]
adidas_list = ['Adidas', 'Yeezy', 'Kanye', 'Ultraboost', 'Ultra Boost', 'FYW', 'Harden']
new_balance_list = ['New Balance', 'NB', 'Balance', '997']
sneaker_list = nike_list + adidas_list + new_balance_list
length = len(sneaker_list) 

nike_count = sneaker_text.count("Nike")
nike_count

for item in sneaker_list:
    name = item + ': '
    count = sneaker_text.count(item)
    print(name, count)