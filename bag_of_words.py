"""
Talia Weiss     MLP Project     March 2013 
bag_of_words.py

This Files main purpose is to calculate bag of word features for all fanfic
objects.  

The dictionary is trained on only the test dataset, and primarily uses nltk

"""
import re
import nltk
import cPickle as pik
from string import punctuation 
from fic_obj import *
from helper_funcs import *
from test_train import load_train_idx
from multiprocessing import Pool, freeze_support, Lock, Manager
from operator import itemgetter
from collections import Counter
import nltk
from sklearn.feature_extraction import DictVectorizer
import numpy as np


def punclist():
    """The list of possible punctuation"""
    punclist = list(punctuation)
    punclist += ["''", '``', '""', '--', '...'] 
    return punclist

def stoplist():
    """The stoplist"""
    stoplist = nltk.corpus.stopwords.words() + ["'s", "n't", "'t", "'ve", "'m", "'d", "'ll"]
    stoplist += punclist()
    return stoplist


def make_dictionary(idx, counter=None):
    wL = get_fic(idx).wordlist
    #fuck common words and punctuation
    tstoplist = stoplist()
    
    wL  = [word.lower() for word in wL if word.lower() not in tstoplist]
    
    #for word in fdist.keys():
    #    if word not in wL_dic.keys():
    #        wL_dic[word] = fdist[word]
    #    else:
    #        wL_dic[word] += fdist[word]
    print idx
    if counter is None:
        return Counter(wL)
    else:
        counter.update(wL)


def EvsG_feat_list(n, lookup=get_default_lookup(), rating=get_default_rating()):
    """Makes a wordlist of the n most frequent words for an Explicit vs Gen 
    classifier"""
    
    #get all training ids:
    train = load_train_idx()

    #subset that list into only 'E' or 'G' fics:
    EG = rating['G'] + rating['E']
    train = [idx for idx in train if idx in EG]

    #Now we need to find the most frequent fics...
    pool = Pool(processes = 4)
    #man = Manager()
    # wL_dict is a dictionary of word : count
    #wL_dict = man.dict()
    #tomap = [(idx, wL_dict) for idx in train]
    #pool.map(make_dictionary, tomap)
    counters = pool.map(make_dictionary, train)
    pool.close()
    pool.join()
    print 'Done!'
    # turn wL_dict into a dictionary 
    #wL_dict = dict(wL_dict.items())
    
    #combine counters
    fin = Counter()
    for c in counters:
        fin += c 
    
    #sort dictionary by value:
    #freq_words = sorted(wL_dict.iteritems(), key=itemgetter(1))
    #freq_words.reverse()
    
    with open('EvG_dict.pik', 'w') as f:
        pik.dump(fin, f)
    
    
    return fin.most_common(n)
    

def EvsG_feat_list_nonpool(n, lookup=get_default_lookup(), rating=get_default_rating()):
    """Makes a wordlist of the n most frequent words for an Explicit vs Gen 
    classifier"""
    
    #get all training ids:
    train = load_train_idx()
    #train = train[0:400]
    #subset that list into only 'E' or 'G' fics:
    EG = rating['G'] + rating['E']
    train = [idx for idx in train if idx in EG]
    #train = train[0:4]
    
    c0 = Counter()
    
    for idx in train:
        make_dictionary(idx, c0)
        print len(c0.keys())
    print 'Done!'

    
    with open('EvG_dict.pik', 'w') as f:
        pik.dump(c0, f)
    
       
    return None
    

def counter_to_array(counter, features):
    numfeat = len(features)
    row_vector = np.zeros((1, numfeat))
    for key in counter.keys():
        index = features.index(key)
        row_vector[0, index] = counter[key]
        
    return row_vector


def to_translate(rating):
    if rating == 'G':
        return 1
    if rating == 'T':
        return 2
    if rating == 'M':
        return 3
    if rating == 'E':
        return 4
    else:
        return 10


def get_bow_features(n, trainset = load_train_idx()):
    """Given a training dataset, loads the learned dictionary and calculates 
    features"""
    lookup = get_default_lookup()
    
    with open('EvG_dict.pik', 'r') as f:
        vocab = pik.load(f)
    #we want our dictionary to be the top n words
    feat = vocab.most_common(n)
    feat = [word for (word, value) in feat]
    
    num_data = len(trainset)
 
    theclass = np.array( (num_data, 1))
    all_feat = np.empty( (num_data, n))
    #now for all trainset, we want to make features
    for i in range(num_data):
        fic = trainset[i]
        wL = get_fic(fic).wordlist
        wL = [word for word in wL if word in feat]
        count = Counter(wL)
        row_vector = counter_to_array(count, feat)
        all_feat[i, :] = row_vector
        theclass[i] = to_translate(lookup[fic].rating[0])
        
    return all_feat, theclass

    
if __name__ == '__main__':
 

    #default lookup tables:
    lookup = get_default_lookup();

    rating = get_default_rating();

    trainset = load_train_idx()
    
    okids = rating['G'] + rating['E']
    
    trainset = [fic for fic in trainset if fic in okids]
    
    trainset = trainset[0:10]
    
    all_feat, theclass = get_bow_features(10, trainset)









