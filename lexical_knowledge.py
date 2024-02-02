import itertools
import nltk
import re

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
        hyp_preds = get_preds(hyp)
    except:
        prem_preds = []
        hyp_preds = []

    for p1, p2 in itertools.product(prem_preds, hyp_preds):  #go thrhough all combinations of words between premise and hypothesis
        try:    #if either don't have a synset
            p1_synset = wn.synsets(p1)[0] 
            p1_args = get_args(p1, prem) #get the arguments of the predicate 
            p2_synset = wn.synsets(p2)[0]
            p2_args = get_args(p2, hyp)
        except:
            continue
        
        if len(p1_args) != len(p2_args):    #skip if the two predicates don't have the same arity 
            continue 

        ## Check for synonyms -> if they have the same synset 
        if p1_synset == p2_synset:
            quants = ""
            for a in p1_args:
                quants += f"all {a}. "
            args = ", ".join(p1_args)
            LK.append(f"{quants}({p1}({args}) -> {p2}({args}))")
            LK.append(f"{quants}({p2}({args}) -> {p1}({args}))")
            continue
        
        ## Check for hyperyms 
        p1_hyper = set([i for i in p1_synset.closure(lambda s:s.hypernyms())])
        if p2_synset in p1_hyper:
            quants = ""
            for a in p1_args:
                quants += f"all {a}. "
            args = ", ".join(p1_args)
            LK.append(f"{quants}({p1}({args}) -> {p2}({args}))")

        p2_hyper = set([i for i in p2_synset.closure(lambda s:s.hypernyms())])
        if p1_synset in p2_hyper:
            quants = ""
            for a in p1_args:
                quants += f"all {a}. "
            args = ", ".join(p1_args)
            LK.append(f"{quants}({p2}({args}) -> {p1}({args}))")
        
    return LK

def get_preds(s : str):
    """
    s: string in NLTK expression proof format 
    """
    expression = Expression.fromstring(s)
    predicates = [str(p) for p in list(expression.predicates())] #list of all predicates 
    
    return list(set(predicates)) #return without duplicates 

def get_args(pred : str, s : str) -> list:
    """
    s: string in NLTK expression proof format 
    Get the arguments of a specific predicate pred in a string
    """
    arguments = re.findall(f"{pred}\((.*?)\)", s)[0]
    argument_list = arguments.split(", ")

    return argument_list