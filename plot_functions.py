# -*- coding: utf-8 -*-
"""
FILENAME: plot_functions.py
PROJECT: Sneaker Website Analysis
DATE CREATED: 15-Nov-19
DATE UPDATED: 15-Nov-19
"""

import requests
import time
import pandas as pd
import datetime
import pprint
from datetime import date 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def bar_chart(df, x_axis, y_axis, title):
    '''
    NAME: bar_chart
    PURPOSE: given a dataframe, two columns, and a title plot a bar chart
    COMMENTS: commented out color code lines
    '''
    
    color_list = ['palegreen','lightsteelblue','wheat','turquoise','silver', 'salmon','palegreen', 'peachpuff']
    # create a new dataframe with the two provided categories
    sliced_df = df[[x_axis,y_axis]]
    summed_df = sliced_df.groupby([x_axis]).sum()
    
    sorted_df = summed_df.sort_values('count', ascending = False)
    master_df = sorted_df.reset_index()
    
    x_val = master_df[x_axis]
    y_val = master_df[y_axis]
    
    x_length = len(x_val)
    
    # begin bar chart 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #cr = ['red', 'grey', 'blue', 'green', 'orange']
    cr = color_list[:x_length]
    ax.bar(x_val, y_val, align='center', color = cr)
    #ax.bar(x_val, y_val, align='center')
    chart_title = title + ' Category Chart'
    ax.title.set_text(chart_title)
    plt.show()