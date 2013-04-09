""" 
Talia Weiss     MLP Project     April 2013 
helper_funcs.py

This File contains functions/classes that are useful for looking up and loading
the parsed data
"""     
       
import cPickle as pik
import os, errno
from common import mkdir_p
#import re
from fic_obj import Fanfic, Lookup     
       
def get_default_lookup():
    """returns the default lookup dictionary in lookup_table.pik, probably made
    by data_extract.py"""
    
    PATH = '/home/talcat/Desktop/Classes/MLP/ao3scrape/lookup_table.pik'
    
    with open(PATH, 'r') as f:
        table = pik.load(f)
        
    return table

def get_default_cat():
    """returns the default category lookup table made by data_extract.py"""
    
    PATH = '/home/talcat/Desktop/Classes/MLP/ao3scrape/category.pik'
    
    with open(PATH, 'r') as f:
        table = pik.load(f)
        
    return table


def get_default_rating():
    """returns the default rating lookup table made by data_extract.py"""
    
    PATH = '/home/talcat/Desktop/Classes/MLP/ao3scrape/rating.pik'
    
    with open(PATH, 'r') as f:
        table = pik.load(f)
        
    return table

        
def get_fic(id_num, lookup=get_default_lookup()):
    """Given a fic id, will return the fic object loaded into memory"""
    
    try:
        look = lookup[id_num] 
    except KeyError:
        print 'Not a valid fic id'
        return None
        
    with open(look.path, 'r') as f:
        fic = pik.load(f)
        
    return fic
        


