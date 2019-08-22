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
import csv
import pandas as pd
import datetime
import pprint
from datetime import date 
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
        self.site_df = pd.DataFrame(columns = ['dtg', 'date','year', 'month', 'day', 'category_name', 'item', 'count'])
        
        self.soup = ''
        self.hyperlink_list = ''
        self.paragraph_list = ''
        self.bold_list = ''
        
        self.nike_site_count = 0
        self.adidas_site_count = 0
        self.reebok_site_count = 0
        self.new_balance_site_count = 0
        self.puma_site_count = 0

        self.nike_master = ['Nike', 'Jordan', 'Converse']
        # ['Nike', 'Air', 'Max', 'Jordan', 'Zoom', 'React', 'Shox', 'ACG', 'Max Plus', 'Joyride', 'Tinker', 'Force', 'Westbrook', 'Kyrie','Lebron', 'Durant', 'SB', 'Air Max 90', 'Air Max 97', 'Air Max 1', 'Kyrie', 'Air Max 270', 'Travis Scott' ]
        self.adidas_master = ['Adidas', 'Reebok', 'ADIDAS', 'Yeezy', 'Kanye']
        # ['Adidas', 'ADIDAS', 'adidas', 'Yeezy', 'Kanye', 'Ultraboost', 'EQT', 'NMD', 'Ultra Boost', 'FYW', 'Harden']
        self.new_balance_master = ['New Balance', 'NB']
        # ['New Balance', 'NB', 'Balance', '997', '801']
        self.puma_master = ['Puma', 'Cell Venom']
        #['Puma', 'Cell Venom', 'Thunder Spectre', 'Clyde Court']

        self.sneaker_list = self.nike_master + self.adidas_master + self.new_balance_master + self.puma_master
        self.length = len(self.sneaker_list)         
        
    def site_calculate(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, "html.parser")
        
        print("\nConsolidating all hyperlinks and paragraphs for", self.name)        
        self.hyperlink_list = self.soup.findAll('a')
        self.paragraph_list = self.soup.findAll('p')
        self.bold_list = self.soup.findAll('b')
        
        self.site_text = self.soup.get_text()
        print("\nConverting ", self.name, " to text file ... \n")
        
        self.lines = [self.site_text.lower() for line in self.site_text]
        print("\nCalculating individual counts: " )
        
        index_num = 0

        for item in self.sneaker_list:
            name = item + ': '
            count = self.site_text.count(item)
            today = date.today()
            dtg = datetime.datetime.now()
            year = dtg.year
            month = dtg.month
            day_num = dtg.day

            category = ''
            
            if count > 0:
                if item in self.nike_master:
                    self.nike_site_count += count
                    category = 'Nike'
                elif item in self.adidas_master:
                    self.adidas_site_count += count
                    category = 'Adidas'
                elif item in self.new_balance_master:
                    self.new_balance_site_count += count
                    category = 'New Balance'
                elif item in self.puma_master:
                    self.puma_site_count += count
                    category = 'Puma'
                else: 
                    0
            else: 
                if item in self.nike_master:
                    category = 'Nike'
                elif item in self.adidas_master:
                    category = 'Adidas'
                elif item in self.new_balance_master:
                    category = 'New Balance'
                elif item in self.puma_master:
                    category = 'Puma'
                else: 
                    0                
            self.site_df.loc[index_num] = [dtg, today, year, month, day_num, category, item, count]        
            print(name, count)
            index_num += 1
            
    def display_info(self):
        print("\nCalculating total counts by shoe company...")
        print("Total Nike mentions: ", self.nike_site_count)
        print("Total Adidas mentions: ", self.adidas_site_count)
        print("Total New Balance mentions: ", self.new_balance_site_count)
        print("Total Puma mentions: ", self.puma_site_count)      
        print(self.site_df)      
    
    def display_links(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.hyperlink_list)
    
    def display_paragraphs(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.paragraph_list)
        
    def display_bold(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.bold_list)  
#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 2: Execution area --------------------------#
#-----------------------------------------------------------------------------#

sneaker_news = sneaker_site('sneaker_news', 'https://sneakernews.com/')
sneaker_news.site_calculate()
sneaker_news.display_info()
sneaker_news.display_links()
sneaker_news.display_paragraphs()
sneaker_news.display_bold()

kicks_on_fire = sneaker_site('kicks_on_fire', 'https://www.kicksonfire.com/')
kicks_on_fire.site_calculate()
kicks_on_fire.display_info()

sole_collector = sneaker_site('sole_collector', 'https://solecollector.com/')
sole_collector.site_calculate()
sole_collector.display_info()

hypebeast = sneaker_site('hypebeast', 'https://hypebeast.com/')
hypebeast.site_calculate()
hypebeast.display_info()
