import pandas as pd 
from nltk.sem.logic import Expression, Variable

def get_wrong_items(results : pd.DataFrame):
    """
    Returns all wrongly classified items of an evaluation dataframe 
    """
    wrong_e = "label == 'e' & (e_pred == False | c_pred == True)"
    wrong_c = "label == 'c' & (c_pred == False | e_pred == True)"
    wrong_n = "label == 'n' & (e_pred == True | c_pred == True)"
    wrong_items_e = results.query(wrong_e)
    wrong_items_c = results.query(wrong_c)
    wrong_items_n = results.query(wrong_n)

    return wrong_items_e, wrong_items_c, wrong_items_n 

def get_correct_items(results : pd.DataFrame):
    """
    Returns all correctly classified items of an evaluation dataframe 
    """
    correct_e = "label == 'e' & (e_pred == True & c_pred == False)"
    correct_c = "label == 'c' & (c_pred == True & e_pred == False)"
    correct_n = "label == 'n' & (e_pred == False & c_pred == False)"
    correct_items_e = results.query(correct_e)
    correct_items_c = results.query(correct_c)
    correct_items_n = results.query(correct_n)

    return correct_items_e, correct_items_c, correct_items_n 

def get_fol_expressions(df : pd.DataFrame):
    """
    df: a dataframe with columns 'fol_ps' and 'fol_h' 
    returns: list of all fol formulas in p_fol and c_fol (as strings)
    """
    prem_fols = list(df['fol_ps'])
    hyp_fols = list(df['fol_h'])

    return prem_fols + hyp_fols

def get_free_vars(df : pd.DataFrame, mult_p = False):
    """
    df: a dataframe with columns 'fol_ps', 'fol_h', 'label', 'e_pred', and 'c_pred'" 
    mult_p = if True it expects 2 prem columns 'fol_ps' and 'p_2_fol'
    returns: dict of problems that were translated with free variables. key = problem id, value = (list of free variables, gold label, e_pred, c_pred)
    """
    all_free_vars = {}

    for id, row in df.iterrows():
        e = Expression.fromstring(row['fol_ps'])
        free = e.free()
        if free:
            all_free_vars[id] = (free, row['label'], row['e_pred'], row['c_pred'])
        if mult_p:
            e = Expression.fromstring(row['p_2_fol'])
            free = e.free()
            if free:
                all_free_vars[id] = (free, row['label'], row['e_pred'], row['c_pred'])
        e = Expression.fromstring(row['fol_h'])
        free = e.free()
        if free:
            all_free_vars[id] = (free, row['label'], row['e_pred'], row['c_pred'])

    return all_free_vars