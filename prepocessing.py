import re 

class preprocessing:
    
    def fol2nltk(s:str) -> str:
        s = re.sub('∧', '&', s)
        s = re.sub('∃(\S*)', 'exists \\1.', s) #counts all chars after quantifier until there is white space as the var  
        s = re.sub('∀(\S*)', 'all \\1.', s)
        return s 