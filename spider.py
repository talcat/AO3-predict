import mechanize as mech
import re
import os, errno
from multiprocessing import Pool, freeze_support

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def ao3_search(rating, month_start, month_end):
    """Generates the url for searching AO3 database.  Only controlling:
    rating = {'G', 'T', 'M', 'E', 'NoRate', 'All'}
    month_start = NUM
    month_end = NUM
      i.e. month_end - month_start months ago """
    GEN = 10
    TEEN= 11
    MATURE = 12
    EXPLICIT = 13
    NORATE = 9
    LANG_ENG = 1
    
    dic = {'G': GEN, 'T':TEEN, 'M': MATURE, 'E':EXPLICIT, 'NoRate':NORATE, 
            'All':'' }
    
    if rating in dic:
        rating = dic[rating]
    else:
        return 'Error: not valid rating choice'
    
    
    search_res = "".join(["http://archiveofourown.org/works/search?", 
      "&work_search[revised_at]=", "%d-%d+months+ago" %(month_end, month_start), 
      "&work_search[complete]=1", "&work_search[word_count]=%3E1000", 
      "&work_search[language_id]=", "%d" %(LANG_ENG), 
      "&work_search[rating_ids]=", "%s" %(rating), 
      "&work_search[freeform_names]=-Illustrated", "&commit=Search"])

    return search_res


class AO3spider:
    """This is a spider than trolls ao3 and downloads stuff. Will only download
    complete works >1000 words that do not have the illustrated tag.  Allows 
    definition of rating and months to search so I can multiprocess it if I need
    too.  """
    def __init__ (self, (month_start, month_end, rating)):
        self.search_url_base = ao3_search(rating, month_start, month_end)
        self.current_search = self.search_url_base
        self.br=mech.Browser()
        self.br.set_handle_robots(False)
        self.done = False
        self.br.open(self.search_url_base)
        self.path = '%s_%sto%s' %(rating, month_start, month_end)
        mkdir_p(self.path)
        
        self.run_all()
        
    def next_page(self):
        if self.current_page_id() is not 'search':
            self.br.open(self.current_search)
        
        #this will fail if we are on the last page of search results    
        try:
            self.br.follow_link(text='Next \xe2\x86\x92')
            print "Next Page reached"
        except mech.LinkNotFoundError:
            self.done = True
            print "No More Pages"
            
        #so you can easily go to next page of search results
        self.current_search = self.br.geturl()
        
               
    def current_page_id(self):
        """returns whether it is on a search page, fic page, or html page"""
        title = self.br.title()
        url = self.br.geturl()
        
        if re.search(r'Search Works', title) is not None:
            return 'search'
        elif re.search(r'/works/\d+', url) is not None:
            return 'fic'
        elif re.search(r'/downloads/.+\.html', url) is not None:
            return 'html'
        else:
            return 'error'
    
    def get_fic(self, link, id_num):
        #go to the link of the fic
        self.br.follow_link(link)
        
        #check to see if on the adult content page:
        try:  #because find_link will raise an LinkNotFound error >_<
            if (self.br.title() == 'Show Work | Archive of Our Own' and
               self.br.find_link(text='Proceed') is not None):
               
               self.br.follow_link(text='Proceed') 
        except:
            print "Cookie Saved somehow"       
        #get the fics html
        htmllink = self.br.find_link(text='HTML')
        #go to it
        htmlpage = self.br.follow_link(htmllink)
        with open('%s/%s.html' %(self.path, id_num), 'w') as f:
            f.write(htmlpage.get_data()) 
            
        #go back to search page:
        self.br.open(self.current_search)

    
    def run_per_page(self):
           
        list_fics = [link for link in self.br.links() if re.search(r'^/works/\d+\Z', link.url) is not None]
        
        for fic in list_fics:
            id_num = re.search(r'\d+\Z', fic.url).group(0)
            print fic.url
            self.get_fic(fic, id_num)
    

    def run_all(self):
        #go to start page
        self.br.open(self.search_url_base)
        #while we are still running:
        while not self.done:
            print self.done
            self.run_per_page()
            self.next_page()
                
            
        
def run():
    #month_start, month_end, rating
    torun = [ (5, 3, 'G'), (5, 3, 'T'), (5, 3, 'M'), (5, 3, 'E') ]
            
    pool = Pool(processes=4)
    pool.map(AO3spider, torun)
    
    
    

