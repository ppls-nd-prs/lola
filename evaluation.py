import pandas as pd 
from nltk.sem.logic import Expression, Variable

def get_wrong_items(results : pd.DataFrame):
    wrong_e = "label == 'e' & (e_pred == False | c_pred == True)"
    wrong_c = "label == 'c' & (c_pred == False | e_pred == True)"
    wrong_n = "label == 'n' & (e_pred == True | c_pred == True)"
    wrong_items_e = results.query(wrong_e)
    wrong_items_c = results.query(wrong_c)
    wrong_items_n = results.query(wrong_n)

    return wrong_items_e, wrong_items_c, wrong_items_n 

def get_correct_items(results : pd.DataFrame):
    correct_e = "label == 'e' & (e_pred == True & c_pred == False)"
    correct_c = "label == 'c' & (c_pred == True & e_pred == False)"
    correct_n = "label == 'n' & (e_pred == False & c_pred == False)"
    correct_items_e = results.query(correct_e)
    correct_items_c = results.query(correct_c)
    correct_items_n = results.query(correct_n)

    return correct_items_e, correct_items_c, correct_items_n 

def get_fol_expressions(df : pd.DataFrame):
    """
    df: a dataframe with olumns 'p_fol' and 'h_fol" 
    returns: list of all fol formulas in p_fol and c_fol (as strings)
    """
    prem_fols = list(df['p_1_fol'])
    hyp_fols = list(df['h_fol'])

    return prem_fols + hyp_fols

def get_free_vars(df : pd.DataFrame):
    """
    df: a dataframe with columns 'p_fol', 'h_fol', 'label', 'e_pred', and 'c_pred'" 
    returns: dict of problems that were translated with free variables. key = problem id, value = (list of free variables, gold label, e_pred, c_pred)
    """
    all_free_vars = {}

    for id, row in df.iterrows():
        e = Expression.fromstring(row['p_1_fol'])
        free = e.free()
        if free:
            all_free_vars[id] = (free, row['label'], row['e_pred'], row['c_pred'])
        e = Expression.fromstring(row['h_fol'])
        free = e.free()
        if free:
            all_free_vars[id] = (free, row['label'], row['e_pred'], row['c_pred'])

    return all_free_vars