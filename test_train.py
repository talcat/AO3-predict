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
from collections import OrderedDict

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
           

def fix_rateandcat_dics():
    """Using the lookup table as law, will ensure that the rating dictionary and
    the category dictionary contains all fics in the lookup table"""
    
    lookup = get_default_lookup()
    rating = get_default_rating()
    cat = get_default_cat()
    
    for idx in lookup.keys():
        rate = lookup[idx].rating[0]
        if idx not in rating[rate]:
            rating[rate] += [idx]
            
        cats = lookup[idx].cat
        for thecat in cats:
            if idx not in cat[thecat]:
                cat[thecat] += [idx]
    with open('rating.pik', 'w') as f:
        pik.dump(rating, f)
        
    with open('category.pik', 'w') as f:
        pik.dump(cat, f)

    
    
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
    
def corr_cat_with_rate(data):
    """Given a list of fic ids (data), makes a piechart for each rating about the
    distribution of relationship categories."""
    
    cat = get_default_cat()
    rating = get_default_rating()
    lookup = get_default_lookup()
    
    E_cat = OrderedDict([('G',0), ('S',0), ('FS',0), ('H',0), ('M',0), ('O',0)])
    M_cat = OrderedDict([('G',0), ('S',0), ('FS',0), ('H',0), ('M',0), ('O',0)])
    T_cat = OrderedDict([('G',0), ('S',0), ('FS',0), ('H',0), ('M',0), ('O',0)])
    G_cat = OrderedDict([('G',0), ('S',0), ('FS',0), ('H',0), ('M',0), ('O',0)])
    overall = OrderedDict([('G',0), ('S',0), ('FS',0), ('H',0), ('M',0), ('O',0)])
      
    for fic in data:
        if fic in rating['E']:
            for thecat in lookup[fic].cat:
                E_cat[thecat] += 1
        elif fic in rating['M']:
            for thecat in lookup[fic].cat:
                M_cat[thecat] += 1
        elif fic in rating['T']:
            for thecat in lookup[fic].cat:
                T_cat[thecat] += 1
        elif fic in rating['G']:
            for thecat in lookup[fic].cat:
                G_cat[thecat] += 1
        for thecat in lookup[fic].cat:
            overall[thecat] += 1
    
    plt.figure()
    plt.pie( E_cat.values(), explode=None, 
          labels=['Gen', 'Slash', 'Femslash', 'Het', 'Multi', 'Other'], autopct='%1.1f%%')
    plt.title('Explicit Breakdown')
    plt.savefig('explicitvscat.png')
    
    plt.figure()
    plt.pie( T_cat.values(), explode=None, 
          labels=['Gen', 'Slash', 'Femslash', 'Het', 'Multi', 'Other'], autopct='%1.1f%%')
    plt.title('Teen Breakdown')
    plt.savefig('teenvscat.png')
    
    plt.figure()
    plt.pie( M_cat.values(), explode=None, 
         labels=['Gen', 'Slash', 'Femslash', 'Het', 'Multi', 'Other'], autopct='%1.1f%%')
    plt.title('Mature Breakdown')
    plt.savefig('maturevscat.png')
    
    plt.figure()
    plt.pie( G_cat.values(), explode=None, 
          labels=['Gen', 'Slash', 'Femslash', 'Het', 'Multi', 'Other'], autopct='%1.1f%%')
    plt.title('Gen Breakdown')
    plt.savefig('genvscat.png')
    
    print overall
    print overall.values()
    plt.figure()
    plt.pie( overall.values(), explode=None, 
          labels=['Gen', 'Slash', 'Femslash', 'Het', 'Multi', 'Other'], autopct='%1.1f%%')
    plt.title('Training Set Category Breakdown')
    plt.savefig('catoverall.png')

