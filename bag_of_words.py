"""
Talia Weiss     MLP Project     March 2013 
bag_of_words.py

This Files main purpose is to calculate bag of word features for all fanfic
objects.  

The dictionary is trained on only the test dataset, and primarily uses nltk

"""
import re
from bs4 import BeautifulSoup, SoupStrainer
from unidecode import unidecode #deals with unicode punctuation, etc
import nltk
import cPickle as pik
from string import punctuation as punclist
from fic_obj import *
from multiprocessing import Pool, freeze_support, Lock, Manager






def count_words((idx, num_count)):
    wl = fixed_word_list(idx)
    num_count[0] += len(wl)


def make_dictionary((idx, wL_dic)):
    wL = fixed_word_list(idx)
    wL_dic[idx] = wL
    print idx
    return None

if __name__ == '__main__':
    punclist = list(punclist)
    punclist += ["''", '``', '""', '--'] 

    stoplist = nltk.corpus.stopwords.words() + ["'s", "n't", "'t", "'ve", "'m", "'d", "'ll"]

    #default lookup tables:
    lookup = get_default_lookup();

    rating = get_default_rating();

    #get all training ids...
    with open('traindata.pik', 'r') as f:
        traindata = pik.load(f)

    # Get appended list of all words
    num_words = 0 
    #for f_id in traindata:
    #  wl = fixed_word_list(f_id)
    #  num_words += len(wl)


         
    pool = Pool(processes = 4)
    man = Manager()
    numwords = man.list()
    numwords = [0]
    wL_dict = man.dict()
    tomap = [(idx, wL_dict) for idx in traindata]
    pool.map(make_dictionary, tomap)
   
    print 'All Done'
    with open('wordl_dict.pik', 'w') as f:
         pik.dump(dict(wL_dict.items()), f)
    print 'Saved Successfully?'














