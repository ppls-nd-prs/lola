import pandas as pd 
from nltk.sem.logic import Expression

def get_wrong_items(results : pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame) :
    wrong_e = "label == 'e' & (e_pred == False | c_pred == True)"
    wrong_c = "label == 'c' & (c_pred == False | e_pred == True)"
    wrong_n = "label == 'n' & (e_pred == True | c_pred == True)"
    wrong_items_e = results.query(wrong_e)
    wrong_items_c = results.query(wrong_c)
    wrong_items_n = results.query(wrong_n)

    return wrong_items_e, wrong_items_c, wrong_items_n 

def get_fol_expressions(df : pd.DataFrame) -> [str]:
    """
    data: a dataframe with e.g. columns 'p_fol' and 'h_fol" 
    returns: list of all fol formulas in p_fol and c_fol (as strings)
    """
    prem_fols = list(df['p_fol'])
    hyp_fols = list(df['h_fol'])

    return prem_fols + hyp_fols