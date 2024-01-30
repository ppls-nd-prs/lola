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
from nltk.sem.logic import Expression

def get_hypo_syn_lk(prem : str, hyp : str):
    # Check if there is a hyponym/hypernym relation between two words based on WordNet.
    LK = [] #list to save all relevant lexical knowledge 

    try:
        prem_preds = get_preds(prem)
        # print(prem_preds)   #DEBUG
        hyp_preds = get_preds(hyp)
        # print(hyp_preds)    #DEBUG 
    except:
        prem_preds = []
        hyp_preds = []

    for p1, p2 in itertools.product(prem_preds, hyp_preds):  #go thrhough all combinations of words between premise and hypothesis
        # print(p1, p2)   #DEBUG 
        try:    #if either don't have a synset
            p1_synset = wn.synsets(p1)[0] 
            # print(p1_synset)    #DEBUG
            p2_synset = wn.synsets(p2)[0]
            # print(p2_synset)    #DEBUG
        except:
            # print(f"no synset for either {p1} or {p2}") #DEBUG 
            continue

        ## Check for synonyms -> if they have the same synset 
        if p1_synset == p2_synset:
            LK.append(f"all x. ({p1}(x) -> {p2}(x))")
            LK.append(f"all x. ({p2}(x) -> {p1}(x))")
        
        ## Check for hyperyms 
        p1_hyper = set([i for i in p1_synset.closure(lambda s:s.hypernyms())])
        if p2_synset in p1_hyper:
            LK.append(f"all x. ({p1}(x) -> {p2}(x))")
        p2_hyper = set([i for i in p2_synset.closure(lambda s:s.hypernyms())])
        if p1_synset in p2_hyper:
            LK.append(f"all x. ({p2}(x) -> {p1}(x))")
        
    return LK

def get_preds(s : str):
    """
    s: string in NLTK expression proof format 
    """
    expression = Expression.fromstring(s)
    predicates = [str(p) for p in list(expression.predicates())] #list of all predicates 
    
    return list(set(predicates)) #return without duplicates 