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
from lexical_knowledge import get_preds, get_args

class preprocessing:
    
    def fol2nltk(s:str) -> str:
        s = re.sub('∧', '&', s)
        s = re.sub('∨', '|', s)
        s = re.sub('-', '_', s)
        s = re.sub('∃(\S\d*)', 'exists \\1.', s) #counts all chars after quantifier until there is white space as the var  
        s = re.sub('∀(\S\d*)', 'all \\1.', s)
        s = re.sub('→', '->', s)
        s = re.sub('¬', 'not ', s)
        return s 

class modifying:
    
    def all2exists(s:str) -> str:
        """
        Replace all instances of '∀' in s, with '∃' 
        Note: this is before the strings are in NLTK friendly format 
        """
        s = re.sub('∀', '∃', s)
        return s 
    
    def imp2con(s:str) -> str:
        """
        Replace all instances of '→' in s, with '∧' 
        Note: this is before the strings are in NLTK friendly format 
        """
        s = re.sub('→', '∧', s)
        return s 
    
    def e_i2c(s:str) -> str:
        """
        Replace all instances of '→' in s, with '∧' if main quantifier is '∃'
        Note: this is before the strings are in NLTK friendly format 
        """
        if s[0] == '∃':
            s = re.sub('→', '∧', s)
        return s 
    
    def split_verb(s:str) -> str:
        """
        Split predicates of the form "VerbObject(x)" into "∃y Verb(x,y) ∧ Object(y)"
        """
        try:
            s_nltk = preprocessing.fol2nltk(s)
            preds = get_preds(s_nltk)
            
            preds_info =[]
            for p in preds:
                parts = re.findall('[A-Z][^A-Z]*', p)
                args = get_args(p, s_nltk)
                preds_info.append((p, parts, args))
            # print("preds info: ", preds_info)   #DEBUG
            
            for pred, parts, args in preds_info:
                if len(parts) == 2 and len(args) == 1: #only split predicates of 2 words, with 1 argument 
                    arg = args[0]
                    old = f"{pred}\({arg}\)" #old predicate with argument 
                    # print("old: ", old) #DEBUG
                    new = f"({parts[0]}({arg}, z500) ∧ {parts[1]}(z500))"
                    # print("new: ", new) #DEBUG
                    s = re.sub(old, new, s)
                    s = "∃z500 " + s 

            return s 

        except: #if it can't be turned into nltk expression (in get_preds), don't do anything 
            return s 
        
    def split_adj(s:str) -> str:
        """
        Split predicates of the form "AdjectiveNoun(x)" into "Adjective(x) ∧ Noun(y)"
        """
        try:
            s_nltk = preprocessing.fol2nltk(s)
            preds = get_preds(s_nltk)
            
            preds_info =[]
            for p in preds:
                parts = re.findall('[A-Z][^A-Z]*', p)
                args = get_args(p, s_nltk)
                preds_info.append((p, parts, args))
            # print("preds info: ", preds_info)   #DEBUG
            
            for pred, parts, args in preds_info:
                if len(parts) == 2 and len(args) == 1: #only split predicates of 2 words, with 1 argument 
                    arg = args[0]
                    old = f"{pred}\({arg}\)" #old predicate with argument 
                    # print("old: ", old) #DEBUG
                    new = f"{parts[0]}({arg}) ∧ {parts[1]}({arg})"
                    # print("new: ", new) #DEBUG
                    s = re.sub(old, new, s)

            return s 

        except: #if it can't be turned into nltk expression (in get_preds), don't do anything 
            return s    