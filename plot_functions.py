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
import seaborn as sns
import datetime
import pprint
import plotly.express as px
import plotly.offline as po
from datetime import date 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def bar_chart(df, x_axis, y_axis, title):
    '''
    NAME: bar_chart function
    PURPOSE: given a dataframe, two columns, and a title plot a bar chart
    COMMENTS: only allows one (1) x categorical variable and one (1) x quantifiable variable
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
    fig = plt.figure(figsize = (12,8))
    ax = fig.add_subplot(111)
    #cr = ['red', 'grey', 'blue', 'green', 'orange']
    cr = color_list[:x_length]
    ax.bar(x_val, y_val, align='center', color = cr)
    #ax.bar(x_val, y_val, align='center')
    chart_title = title + ' Category Chart'
    ax.title.set_text(chart_title)
    plt.show()
    
def pie_chart(df, x_axis, y_axis, title):
    '''
    NAME: pie_chart function
    PURPOSE: given a dataframe, two columns, and a title, plot a pie chart
    COMMENTS: only allows one (1) x categorical variable and one (1) x quantifiable variable
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
    cr = color_list[:x_length]
    plt.figure(figsize = (12,8))
    plt.pie(y_val, labels=x_val, colors=cr, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()


def linear_reg_sns(df):
    X = (df.index -  df.index[0]).days.reshape(-1, 1)
    ax = sns.regplot(x="total_bill", y="tip", data=tips)

def timeseries_line_chart(df, shoe_company, title):
    '''
    NAME: timeseries_line_chart function
    PURPOSE: given a dataframe, a filtered column value, and a title, plot a timeseries chart
    COMMENTS: only allows one (1) x categorical variable and one (1) x quantifiable variable
    '''
    cond1 = df['category_name'] == shoe_company
    temp_df = df[cond1]
    filtered_df = temp_df[['date','count']]
    group_df = filtered_df.groupby(['date']).sum().reset_index()
    plot_df = pd.pivot_table(group_df,values='count',index='date')
    fig = plot_df.plot(figsize = (12,8), title = title)
    return fig 

def multiple_line_series(df, title):
    #color_list = ['palegreen','lightsteelblue','wheat','turquoise','silver', 'salmon','palegreen', 'peachpuff']
    temp_df = df[['date','category_name','count']]
    group_df = temp_df.groupby(['date','category_name']).sum().reset_index()
    plot_df = pd.pivot_table(group_df,values='count',index='date',columns='category_name')
    #plot_df = temp_df.pivot(index='date', columns='category_name', values='count')
    #return df
    plot_df.plot(figsize = (12,8), title = title)
    

def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig
