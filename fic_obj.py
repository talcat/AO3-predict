""" 
Talia Weiss     MLP Project     March 2013 
fic_obj.py

This File contains functions/classes for turning fics into objects and making
feature objects out of them
"""
import re
from bs4 import BeautifulSoup, SoupStrainer
from unidecode import unidecode #deals with unicode punctuation, etc
import nltk
import cPickle as pik


class Fanfic(object):
    
    def __init__(self, filename):
        """Given the raw HTML, will construct an object including:
        -ID num
        -Month last updated
        -Rating
        -Category (i.e. Relationship class) (list)
        -Word Length
        -Fandom (list)
        -document (fic not including notes/summaries with punctuation)
        -list of words in document (not including notes/summaries)"""
        
        number = re.search(r'\d*\.html', filename).group(0)
        
        self.id = int(re.split(r'\.', number)[0])
        
        with open(filename, 'r') as fic: 
            raw = fic.read()
            
        
        body = SoupStrainer('body')    
        soup = BeautifulSoup(raw, 'lxml', parse_only=body)
        
        self.month = None
        self.rating = None
        self.cat = []
        self.mult_chap = None
        self.wordlen = 0
        self.fandom = None
        self.doc = ''
        self.wordlist = []
                
        self._set_props(soup)
        self._set_wordlist(soup)
        
    def _set_props(self, soup):
        """Finds and sets the meta information of a fic"""
        meta = soup.find('dl', 'tags')
        self.rating = meta.find('dt', text='Rating:').findNext('dd').text 
        
        #can have multiple categories, separated by ','
        cats = meta.find('dt', text = 'Category:').findNext('dd').text
        self.cat = re.split(r',', cats)
        
        #can have multiple fandoms, separated by ','
        fanlist = meta.find('dt', text='Fandom:').findNext('dd').text
        self.fandom = re.split(r',', fanlist)
        
        
        stats = meta.find('dt', text='Stats:').findNext('dd').text
        
        month = re.compile('Completed: \d\d\d\d-(?P<month>\d\d)-\d\d', re.U)
        #Multi chapter fic
        if month.search(stats) != None:
            self.month = int(month.search(stats).group('month'))
            
        else: #single chap fics
            month = re.compile('Published: \d\d\d\d-(?P<month>\d\d)-\d\d', re.U)
            self.month = int(month.search(stats).group('month'))
            
        if re.search(ur'Chapters:', stats) !=None:
            self.mult_chap = True
        else:   
            self.mult_chap = False
            
        wordlen = re.compile('Words: (?P<wordlen>\d*)', re.U)
        self.wordlen = int(wordlen.search(stats).group('wordlen'))
                
        
    def _set_wordlist(self, soup):    
        """defines the actually wordlist (in order) of a fic stripped of tags.
        --> Should be in <div class="userstuff">"""
        
        chapters = soup.findAll("div", {"id":"chapters"})
        
        #Strip html tags and newlines
        if self.mult_chap:
            chapters = chapters[0].findAll("div", {"class":"userstuff"})
            alltext = ''.join(map(lambda x: x.get_text(" ", strip=True), chapters))
        else: 
            alltext = chapters[0].get_text(" ", strip=True)    
        
        #destroy the unicode:
        alltext = unidecode(alltext)
        self.doc = alltext
                
        self.wordlist = self.fixed_word_list()
    
    def fixed_word_list(self):
            
        sentences = nltk.sent_tokenize(self.doc)
        wordlist = map(nltk.word_tokenize, sentences)
        wordlist = [w for sublist in wordlist for w in sublist]
        return wordlist



class Lookup(object):
    """Defines a lookup object to load into a lookup table dictionary"""
    def __init__(self, idx, path, cat, rating):
        self.id = idx
        self.path = path
        self.cat = cat
        self.rating = rating
        

        

