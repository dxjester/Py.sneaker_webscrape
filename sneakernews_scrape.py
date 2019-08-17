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
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

# 1.1 Class Declaration ------------------------------------------------------#
class sneaker_site:
    def __init__ (self, name, url):
        self.name = name
        self.url = url
        self.site_text = ''
        self.lines = ''
        
        self.soup = ''
        self.hyperlink_list = ''
        self.paragraph_list = ''
        
        self.nike_site_count = 0
        self.adidas_site_count = 0
        self.reebok_site_count = 0
        self.new_balance_site_count = 0
        self.puma_site_count = 0

        self.nike_master = ['Nike', 'Air', 'Max', 'Jordan', 'Zoom', 'React', 'Shox', 'ACG', 'Max Plus', 'Joyride', 'Tinker', 'Force', 'Westbrook', 'Kyrie','Lebron', 'Durant', 'SB', 'Air Max 90', 'Air Max 1', 'Kyrie', 'Air Max 270', 'Travis Scott' ]
        self.adidas_master = ['Adidas', 'ADIDAS', 'adidas', 'Yeezy', 'Kanye', 'Ultraboost', 'Ultra Boost', 'FYW', 'Harden']
        self.new_balance_master = ['New Balance', 'NB', 'Balance', '997', '801']
        self.puma_master = ['Puma', 'Cell Venom', 'Thunder Spectre', 'Clyde Court']

        self.sneaker_list = self.nike_master + self.adidas_master + self.new_balance_master + self.puma_master
        self.length = len(self.sneaker_list)         
        
    def site_calculate(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, "html.parser")
        
        print("\nConsolidating all hyperlinks and paragraphs in the webpage \n" )        
        self.hyperlink_list = self.soup.findAll('a')
        self.paragraph_list = self.soup.findAll('p')
        
        self.site_text = self.soup.get_text()
        print("\nConverting ", self.name, " to text file ... \n")
        
        self.lines = [self.site_text.lower() for line in self.site_text]
        print("\nCalculating individual counts: " )
        for item in self.sneaker_list:
            name = item + ': '
            count = self.site_text.count(item)
    
            if count > 0:
                if item in self.nike_master:
                    self.nike_site_count += count
                elif item in self.adidas_master:
                    self.adidas_site_count += count
                elif item in self.new_balance_master:
                    self.new_balance_site_count += count
                elif item in self.puma_master:
                    self.puma_site_count += count     
                else: 
                    0 
            print(name, count)
            
    def display_info(self):
        print("\nCalculating total counts by shoe company...")
        print("Total Nike mentions: ", self.nike_site_count)
        print("Total Adidas mentions: ", self.adidas_site_count)
        print("Total New Balance mentions: ", self.new_balance_site_count)
        print("Total Puma mentions: ", self.puma_site_count)       
        print(self.lines)          
  
#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 2: Execution area --------------------------#
#-----------------------------------------------------------------------------#

sneaker_news = sneaker_site('sneakernews.com', 'https://sneakernews.com/')
sneaker_news.site_calculate()
sneaker_news.display_info()

