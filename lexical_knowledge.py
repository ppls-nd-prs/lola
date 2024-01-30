import itertools
import nltk

## Note: use this block if you get "error loading wordnet ... SSL:CERTIFICATE_VERIFY_FAILED ...""
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
##########
    
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def get_hypo_syn_lk(prem : str, hyp : str):
    # Check if there is a hyponym/hypernym relation between two words based on WordNet.
    LK = [] #list to save all relevant llexical knowledge 

    prem_words = list(set(prem.split())) #list of all words in the sentences, with duplicates removed
    # print(prem_words)   #DEBUG
    hyp_words = list(set(hyp.split()))
    # print(hyp_words)    #DEBUG

    for w1, w2 in itertools.product(prem_words, hyp_words):  #go thrhough all combinations of words between premise and hypothesis
        # print(w1, w2)   #DEBUG 
        w1_synset = wn.synsets(w1)[0] #get most common synset 
        # print(w1_synset)    #DEBUG
        w2_synset = wn.synsets(w2)[0]
        # print(w2_synset)    #DEBUG

        ## Check for synonyms -> if they have the same synset 
        if w1_synset == w2_synset:
            LK.append(f"{w1} == {w2}")
        
        ## Check for hyperyms 
        w1_hyper = set([i for i in w1_synset.closure(lambda s:s.hypernyms())])
        if w2_synset in w1_hyper:
            LK.append(f"{w1} is a {w2}")
        w2_hyper = set([i for i in w2_synset.closure(lambda s:s.hypernyms())])
        if w1_synset in w2_hyper:
            LK.append(f"{w2} is a {w1}")
        
    return LK