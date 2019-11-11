# -*- coding: utf-8 -*-
"""
FILENAME: text_functions.py
PROJECT: Sneaker Website Analysis
DATE CREATED: 10-Nov-19
DATE UPDATED: 10-Nov-19
VERSION: 1.0
"""


#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 1: Import Libraries ------------------------#
#-----------------------------------------------------------------------------#


# 1.1 Normalize String -------------------------------------------------------#

def normalize_string(s):
    '''
    - A function which takes a string as a parameter
    - returns a new string with all characters converted to lower case and
    - all non-alphabetic, non-whitespace characters removed
    '''
    
    assert type (s) is str
    
    essential_chars = [c for c in s.lower() if c.isalpha() or c.isspace()]
    return ''.join(essential_chars)

# 1.2 String to Word list ----------------------------------------------------#
def str_to_word_list(s):
    '''
    - A function which takes a string as a parameter
    - returns a list of words in s
    '''
    
    assert type (s) is str
    return normalize_string(s).split()

# 1.3 Item Sets --------------------------------------------------------------#
def make_itemsets(words):
    '''
    - A function which takes a list of strings as a parameter
    - returns a list of item sets for each word in the provided list
    '''
    return [set(w) for w in words]


