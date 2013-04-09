"""
Talia Weiss     MLP Project     Aprilh 2013 
test/train.py

This file has a lot of dictionary building functions related to the test/train
set.


"""
import cPickle as pik
import re
from fic_obj import *
from helper_funcs import *
from random import shuffle
import matplotlib.pyplot as plt


def segment_test_train():
    """ Segments the data into test/train.  Saves them to a .pik file"""
    lookup = get_default_lookup()


    # Lets randomize all possible fic ids
    all_ids = lookup.keys()
    shuffle(all_ids)

    #now define 1/5 of the dataset as train
    num_ids = len(all_ids)
    test = int(num_ids/5)

    testdata = all_ids[0:test]
    traindata = all_ids[test:-1]

    with open('traindata.pik', 'w') as f:
         pik.dump(traindata, f)

    with open('testdata.pik', 'w') as f:
         pik.dump(testdata, f)

    return traindata, testdata

def load_train_idx():
    """returns the list of train ids"""
    with open('traindata.pik', 'r') as f:
        traindata = pik.load(f)
        
    return traindata

def load_test_idx():
    """returns the list of test ids"""
    with open('testdata.pik', 'r') as f:
        testdata = pik.load(f)
        
    return testdata 
           
    
    
def pie_rating_dist(data, chart_name, chart_title):
    """Given a list of fic ids, saves a piechart of the distribution with title
       chart_title as chart_name.png""" 
    
    rating = get_default_rating()
    r_count = {'G' : 0, 'T' : 0, 'M': 0, 'E' : 0}

    for fic in data:
        if fic in rating['E']:
            r_count['E'] += 1
        elif fic in rating['M']:
            r_count['M'] += 1
        elif fic in rating['T']:
            r_count['T'] += 1
        elif fic in rating['G']:
            r_count['G'] += 1
        else:
            print (get_fic(fic).rating, get_fic(fic).cat, fic)

    plt.figure()
    plt.pie( [r_count['G'], r_count['T'], r_count['M'], r_count['E']], explode=None, 
          labels=['Gen\n%d' %(r_count['G']), 'Teen\n%d' %(r_count['T']), 
          'Mature\n%d' %(r_count['M']), 'Explicit\n%d' %(r_count['E'])], autopct='%1.1f%%')
    plt.title(chart_title)
    plt.savefig('%s.png' %(chart_name))
    

