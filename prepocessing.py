import re 

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
