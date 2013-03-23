""" 
Talia Weiss     MLP Project     March 2013 
data_extract.py

This File contains functions/classes for turning raw HTML into rough features
and classes for further analysis
"""
import cPickle as pik
import os, errno
from common import mkdir_p
from multiprocessing import Pool, freeze_support, Lock, Manager
import re
from fic_obj import Fanfic


def get_all_fic_paths(path_list):
    """Get a list of all abs paths of fics for processing quicker"""
    fic_list = []
    for path in path_list:
        fics = [fic for fic in os.listdir(path) if re.search(r'.*\.html', fic) is not     
                None]
        fics = map(lambda x: '%s%s' %(path, x), fics)
        
        fic_list = fic_list + fics
        
    return fic_list


def worker((lookup, rating, cat, path)):
    """For pickling all Fanfics, and creating a dictionary to lookup where 
    fanfics can be loaded.
    lock = the Lock for the dictionary
    path = path per fic"""
    
    # Make new folder for pickled objects if needed
    fold_name= os.path.basename(os.path.dirname(path))
    
    new_folder = '%s%s' %(fold_name, '_pik')
    
    total_path = os.path.dirname(os.path.dirname(path))
    
    new_dir = '%s%s%s' %(total_path, '/', new_folder)
    
    mkdir_p(new_dir)
    #Make fic object
    # This will skip fics that do not have any relationship category because
    # I scraped wrong
    try:
        fic = Fanfic(path)
        print fic.id
        #save fic as id.pik
        filename = '%s/%s.pik'%(new_dir, fic.id)
        with open(filename, 'w') as f:
            pik.dump(fic, f)
        
        #add to dictionary
        lookup[fic.id] = filename
        
        #rating
        rating[fic.rating[0]]+= [fic.id]
    
        #category:
        multi = False
        if len(fic.cat)>1:
            multi=True
        for c in fic.cat:
            if c == 'M/M':
                cat['S']+= [fic.id]
            if c == 'F/M' or c == 'M/F':
                cat['H']+= [fic.id]
            if c == 'F/F':
                cat['FS']+= [fic.id]
            if c == 'Multi':
                multi = True
            if c == 'Other':
                cat['O']+= [fic.id]
            if c == 'Gen':
                cat['G']+= [fic.id]
        if multi:
            cat['M'] += [fic.id]
    except: pass
    
if __name__ == '__main__':
    manager = Manager() #for sharing a dictionary 
    lookup = manager.dict()
    rating = manager.dict()
    rating['G'] = [] 
    rating['T'] = []
    rating['M'] = []
    rating['E'] = []
    
    cat = manager.dict()
    cat['FS'] = []
    cat['S'] = []
    cat['H'] = []
    cat['O'] = []
    cat['M'] = []
    cat['G'] = []
    
    pool = Pool(processes = 25)
    lock = Lock()
    
    PATHS = ['/home/talcat/Desktop/Classes/MLP/ao3scrape/G_6to5/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/T_3to2/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/M_4to3/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/G_5to4/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/T_6to5/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/M_6to5/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/G_4to3/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/T_4to3/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/E_6to5/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/E_5to4/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/M_3to2/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/E_3to2/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/T_5to4/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/G_3to2/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/E_4to3/',
             '/home/talcat/Desktop/Classes/MLP/ao3scrape/M_5to4/']
             
    #fic_list = get_all_fic_paths(['/home/talcat/Desktop/Classes/MLP/ao3scrape/G_6to5/',
    #         '/home/talcat/Desktop/Classes/MLP/ao3scrape/T_3to2/'])
    
    fic_list = get_all_fic_paths(PATHS)
    
    items = [(lookup, rating, cat, fic) for fic in fic_list]
                
    pool.map(worker, items)
         

    print 'All Done'
    print len(fic_list)
    print len(rating['E']) + len(rating['T']) + len(rating['M']) + len(rating['G'])

    with open('rating.pik', 'w') as f:
        pik.dump(dict(rating.items()), f)
        
    with open('category.pik', 'w') as f:
        pik.dump(dict(cat.items()), f)
        
    with open('lookup_table.pik', 'w') as f:
        pik.dump(dict(lookup.items()), f)
        

    
