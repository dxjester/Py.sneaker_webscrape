# -*- coding: utf-8 -*-
"""
FILENAME: sneakernews_scrape.py
PROJECT: Sneaker Website Analysis
DATE CREATED: 15-Aug-19
DATE UPDATED: 27-NOV-19
VERSION: 1.0
"""


#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 1: Program Setup ---------------------------#
#-----------------------------------------------------------------------------#

# 1.1 Module Import ----------------------------------------------------------#
# import the required modules
import requests
import time
import pandas as pd
import datetime
import pprint
from datetime import date 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# external python files
import plot_functions as pf
import text_functions as tf
# from collections import Counter
# from string import punctuation

# 1.1 Class Declaration ------------------------------------------------------#
class sneaker_site:
    '''
    DESCRIPTION: Purpose of this class is to store website data located from various
        sneaker websites and retrieve pertinent key words from each object's scrape.
        The data scraped is then transformed into a tibble, which is then exported as 
        it's on individual CSV, later utilized for follow-on analytics
    '''
    
    # initialize the class
    def __init__ (self, name, url): # provide the name of the website and the url
        '''
        DESCRIPTION: initialize class with default class arguments
        '''
        self.website_name = name # set the name
        self.url = url # save the url
        self.site_text = '' # value to save the site text for each object
        self.converted_site_text = '' # converting the extracted value to lower case, via the 'text_functions' file
        self.lines = ''
        
        # create a dataframe to store extracted values for each object
        self.site_df = pd.DataFrame(columns = ['website','dtg', 'date','year', 'month', 'day', 'category_name', 'item', 'count'])
        self.site_df['website'] = self.website_name # assign the website name to the entire class dataframe
        
        # creating Beautiful Soup variables to store individual values
        self.soup = '' # variable to store the complete values 
        self.hyperlink_list = '' # variable to store the hyperlinks tags
        self.paragraph_list = '' # variable to store paragraph value tags
        self.bold_list = '' # variable to store bold value tags
        
        # create the site variables to aggregate total counts for each object
        self.nike_site_count = 0
        self.adidas_site_count = 0
        self.reebok_site_count = 0
        self.new_balance_site_count = 0
        self.puma_site_count = 0
        self.vans_site_count = 0

        # default Nike list with different Nike shoe companies
        self.nike_master = ['nike', 'jordan', 'converse'] 
        # ['Nike', 'Air', 'Max', 'Jordan', 'Zoom', 'React', 'Shox', 'ACG', 'Max Plus', 'Joyride', 'Tinker', 'Force', 'Westbrook', 'Kyrie','Lebron', 'Durant', 'SB', 'Air Max 90', 'Air Max 97', 'Air Max 1', 'Kyrie', 'Air Max 270', 'Travis Scott' ]

        # default Adidas list with different Adidas shoe companies
        self.adidas_master = ['adidas', 'reebok', 'adidas', 'kanye', 'yeezy']
        # ['Adidas', 'ADIDAS', 'adidas', 'Yeezy', 'Kanye', 'Ultraboost', 'EQT', 'NMD', 'Ultra Boost', 'FYW', 'Harden']
        
        # default New Balance list 
        self.new_balance_master = ['NB', 'new balance']
        # ['New Balance', 'NB', 'Balance', '997', '801']
        
        # default Puma LIst
        self.puma_master = ['Puma', 'puma']
        #['Puma', 'Cell Venom', 'Thunder Spectre', 'Clyde Court']

        # default Vans list
        self.vans_master = ['Vans','vans']
        
        # concatenante the individual sneaker lists into one master list
        self.sneaker_list = self.nike_master + self.adidas_master + self.new_balance_master + self.puma_master + self.vans_master
        self.length = len(self.sneaker_list)         
        print("{} website object created".format(self.website_name))
    
    # class function to calculate the counts of each sneaker value in the master 'sneaker_list' data structure
    def site_calculate(self):
        '''
        DESCRIPTION: extract each website's raw data and append in the object's dataframe
        '''
        
        # to calculate the time needed to process the function from start to finish
        start_time = time.time() 
        print("\nRetrieving {} text and data ...".format(self.website_name))
        
        # establish connection to the website
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, "html.parser")
        
        # find and categorize all hyperlink (a), paragraph (p), and bold (b) html tags
        print("\nConsolidating all hyperlinks and paragraphs for", self.website_name)        
        self.hyperlink_list = self.soup.findAll('a')
        self.paragraph_list = self.soup.findAll('p')
        self.bold_list = self.soup.findAll('b')
        
        # convert individual Soup categories to text
        self.site_text = self.soup.get_text()
        self.converted_site_text = tf.normalize_string(self.site_text)
        print("\nConverting ", self.website_name, " to text file ... ")
        
        self.lines = [self.site_text.lower() for line in self.site_text]
        print("\nCalculating individual counts: " )
        
        index_num = 0

        # utilize the for loop to iterate over each object and count the .... 
        # ... amount of times a value is depicted in each extraction
        for item in self.sneaker_list:
            
            # allocate object variables as values for the class dataframe
            website = self.website_name
            name = item + ': '
            count = self.converted_site_text.count(item) # count text items
            today = date.today()
            dtg = datetime.datetime.now()
            year = dtg.year
            month = dtg.month
            day_num = dtg.day

            category = ''
            
            # if count > 0 , aggregate the count based on shoe company name
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
                elif item in self.vans_master:
                    self.vans_site_count += count
                    category = 'Vans'
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
                elif item in self.vans_master:
                    category = 'Vans'
                else: 
                    0      
                    
            # append each new row to the class dataframe
            self.site_df.loc[index_num] = [website, dtg, today, year, month, day_num, category, item, count]        
            print(name, count)
            index_num += 1
        
        elapsed_time = time.time() - start_time 
        print("\n{} data ingest completed, total elapsed time: {} seconds\n".format(self.website_name, round(elapsed_time,2)))
        
    def display_info(self):
        '''
        DESCRIPTION: display object information
        '''
        print("\nCalculating total counts by shoe company...")
        print("Total Nike mentions: ", self.nike_site_count)
        print("Total Adidas mentions: ", self.adidas_site_count)
        print("Total New Balance mentions: ", self.new_balance_site_count)
        print("Total Puma mentions: ", self.puma_site_count)      
        print("Total Vans mentions: ", self.vans_site_count)      
        # print(self.site_df)      
        
    def return_df(self):
        '''
        DESCRIPTION: return class dataframe 
        '''
        return self.site_df

    def display_soup(self):
        '''
        DESCRIPTION: display hyperlinks for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.soup)
    
    def display_links(self):
        '''
        DESCRIPTION: display hyperlinks for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.hyperlink_list)
    
    def display_paragraphs(self):
        '''
        DESCRIPTION: display paragraphs for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.paragraph_list)
        
    def display_bold(self):
        '''
        DESCRIPTION: display bold tags for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.bold_list)  
        

#----------------------------------- START -----------------------------------#
#------------------------- PHASE 2: Website Scrape  --------------------------#
#-----------------------------------------------------------------------------#

print("\n Starting Phase 2 ...\n")

# 2.1: SNEAKERNEWS.com ingest and analysis -----------------------------------#
sneaker_news = sneaker_site('sneakernews.com', 'https://sneakernews.com/')
sneaker_news.site_calculate()
sneaker_news.display_info()

#sneaker_news.display_links()
#sneaker_news.display_paragraphs()
#sneaker_news.display_bold()
#sneaker_news.display_soup()

# retrieve master sneakernews.com dataframe
sneaker_news_df = sneaker_news.return_df()
sneaker_news_df.head(10)

# website plotting
pf.bar_chart(sneaker_news_df,'category_name', 'count', 'Sneakernews.com')
pf.pie_chart(sneaker_news_df,'category_name', 'count', 'Sneakernews.com')




# 2.2: SOLECOLLECTOR.com ingest and analysis ---------------------------------#
sole_collector = sneaker_site('Solecollector.com', 'https://solecollector.com/')
sole_collector.site_calculate()
sole_collector.display_info()

#sole_collector.display_links()
#sole_collector.display_paragraphs()
#sole_collector.display_bold()
#sole_collector.display_soup()

# retrieve master sneakernews.com dataframe
sole_collector_df = sole_collector.return_df()
sole_collector_df.head(10)

# website plotting
pf.bar_chart(sole_collector_df,'category_name', 'count', 'Solecollector.com')
pf.pie_chart(sole_collector_df,'category_name', 'count', 'Solecollector.com')



# 2.3: HYPEBEAST.com ingest and analysis -------------------------------------#
hypebeast = sneaker_site('hypebeast.com', 'https://hypebeast.com/')
hypebeast.site_calculate()
hypebeast.display_info()

#hypebeast.display_links()
#hypebeast.display_paragraphs()
#hypebeast.display_bold()
#hypebeast.display_soup()

# retrieve master sneakernews.com dataframe
hypebeast_df = hypebeast.return_df()
hypebeast_df.head(10)

# website plotting
pf.bar_chart(hypebeast_df,'category_name', 'count', 'Hypebeast.com')
pf.pie_chart(hypebeast_df,'category_name', 'count', 'Hypebeast.com')

print("\n End of Phase 2 ...\n")



#----------------------------------- START -----------------------------------#
#------------------- PHASE 3: Data Consolidation & Export --------------------#
#-----------------------------------------------------------------------------#

print("\n Starting Phase 3 ...\n")

# concat the three dataframes into a single, unified dataframe
frames = [sneaker_news_df, sole_collector_df, hypebeast_df]
day_master = pd.concat(frames)
day_master['short_date'] = day_master['dtg'].dt.date
day_master.head(10)

pf.bar_chart(day_master,'category_name', 'count', 'Consolidated Bar Chart Report')
pf.pie_chart(day_master,'category_name', 'count', 'Consolidated Pie Report')

path = '/Users/patrickbenitez/Desktop/GT/Codebook/Git/Py.sneakernews.webscrape/df_exports/'
# Converting date into DD-MM-YYYY format
temp_date = datetime.datetime.today()

file_date = temp_date.strftime('%Y-%m-%d')


# create the full file path
full_path = path + "v2_" +  file_date + ".csv"

# export the file to the /df_exports/ directory
day_master.to_csv(full_path)

print("\nFile successfully exported!")




#----------------------------------- START -----------------------------------#
#---------------------- PHASE 4: CSV Import & Analysis -----------------------#
#-----------------------------------------------------------------------------#

# 4.1: Determine all version 1.0 files located in the 'df_exports' directory--#
import glob # to read in multiple csv files


print("\nRetrieving version 1.0 csv files ...")

csv_list = [] # store values in the list
for csv_file_v1 in glob.glob('df_exports/v1_*.csv'): # only retrieve "v1_" csv files
    csv_list.append(csv_file_v1)
    print (csv_file_v1)
    
for csv_file_v2 in glob.glob('df_exports/v2_*.csv'): # only retrieve "v2_" csv files
    csv_list.append(csv_file_v2)
    print (csv_file_v2)

print("\nTotal amount of files: {}".format(len(csv_list)))



# 4.2: Read in each csv file into the master dataframe -----------------------#
# 4.2.1: read in the local files and aggregate as a single dataframe -#
master_df = pd.DataFrame(columns=['date', 'category_name', 'item', 'count'])

# extract the four columns from each csv file and append to 'master_df'
for csv_file in csv_list:
    temp_df = pd.read_csv(csv_file)
    sliced_df = temp_df[['date', 'category_name', 'item', 'count']]
    master_df = pd.concat([master_df, sliced_df])
    
master_df['count'] = master_df['count'].astype(int)
master_df['date'] = master_df['date'].astype('datetime64[ns]')
master_df.dtypes
master_df.head(25)

# group by sum the master_df dataframe for follow-on analysis
master_sum_df = master_df.groupby(['date','category_name', 'item']).sum().reset_index()
summarized_df = master_sum_df[master_sum_df['count'] != 0]
summarized_df.head(5)

sns.pairplot(summarized_df)

# 4.2.2: Unstack and pairplot the master dataframe for category_name df - #
category_df = master_df[['date','category_name','count']]
category_df = category_df.groupby(['date','category_name']).sum().reset_index()
category_df.head(20)

unstack_category_df = category_df.pivot_table(index = ['date'], 
                                   columns = 'category_name',
                                   values = 'count',
                                   aggfunc='first').reset_index().rename_axis(None, axis=1)

unstack_category_df.tail(50)
sns.pairplot(unstack_category_df) # pairplot the category dataframe

# 4.2.3: Unstack and pairplot the master dataframe for item df - #
item_temp_df = master_df[['date','item','count']]
item2_df = item_temp_df.groupby(['date', 'item']).sum().reset_index()

# remove rows where count is equal to '0'
item_df = item2_df[item2_df['count'] != 0]
item_df.head(20)

unstack_item_df = item_df.pivot_table(index = ['date'],
                                      columns = 'item',
                                      values = 'count',
                                      aggfunc='first').reset_index().rename_axis(None, axis=1)

unstack_item_df.tail(50)
sns.pairplot(unstack_item_df) # pairplot the item dataframe

# 4.2.4: Date and Count dataframe
date_count_temp = master_df[['date','count']]
date_count_df = date_count_temp.groupby('date').sum().reset_index()
date_count_df

date_count_df.set_index('date', inplace=True)
date_count_df.plot()
plt.plot(date_count_df)



# 4.3: Invoke plotting functions to depict visualizations --------------------#
# 4.3.1: plot individual linear regression analysis for each shoe company -#
pf.timeseries_line_chart(master_df, 'Nike', 'Nike Timeseries')
pf.timeseries_line_chart(master_df, 'Adidas', 'Adidas Timeseries')
pf.timeseries_line_chart(master_df, 'New Balance', 'New Balance Timeseries')
pf.timeseries_line_chart(master_df, 'Puma', 'Puma Timeseries')
pf.timeseries_line_chart(master_df, 'Vans', 'Nike Timeseries')

# 4.3.2: sorted bar chart -#
print("\n Displaying total history of shoe company mentions ...")
pf.bar_chart(master_df,'category_name', 'count', 'Historical Bar Chart Report')

# 4.3.3: percentage pie chart -#
print("\n Displaying percentage breakdown by shoe companies...")
pf.pie_chart(master_df,'category_name', 'count', 'Historical Pie Report')

# 4.3.4: time series line chart categorized by shoe company -#
print("\n Displaying timeseries summary by shoe company ...")
pf.multiple_line_series(master_df, 'Historical Timeseries')


print("\n End of Program!")

# "If you and Chuck Norris both have 5 dollars, he still has more money that you."
# --------------------------- END OF PROGRAM ---------------------------------#





# TESTING AREA ---------------------------------------------------------------#

test_text = 'This is a test STRING Value for #$%&#@$ text_functions.py file.'
normalize_test_text = tf.normalize_string(test_text)
print(normalize_test_text)
