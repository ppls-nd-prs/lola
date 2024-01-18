import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing
from datasets import load_dataset, concatenate_datasets
import json
import nltk
import pandas as pd
import re
import os
from data_transformations import prepare_for_translation

#locate prover9
PROVER9_BIN = "./prover9/bin"
print(prover9_prove(PROVER9_BIN, "some y. man(y)", ["man(Alex)"]))

def negated(fol_string):
    return "not " + fol_string

def evaluate(translation_dict,dataset,columns,judgment_dict,dataset_name: str):
    '''
    columns should have format [premise-column-name,hypothesis-column-name,
    label-column-name]
    judgment_dict should have format {[value]:"e", [value]:"n",
    [value]:"c"}.
    Returns a pandas dataframe with columns p_nl, h_nl, p_fol, h_fol, label, e_pred, c_pred
    '''
    #TODO: allow for multiple premises
    df = pd.DataFrame({'p_nl':[],'h_nl':[],'p_fol':[],'h_fol':[],'label':[],'e_pred':[],
                       'c_pred':[]})
    e_df = pd.DataFrame({'nl_p':[],'nl_h':[],'exception':[]})
    for datapoint in dataset:
        dat_temp_dict = {}
        e_temp_dict = {}
        # get premise and hypothesis natural string representation
        nl_premise = datapoint[columns[0]]
        dat_temp_dict['p_nl'] = nl_premise
        nl_hypothesis = datapoint[columns[1]]
        dat_temp_dict['h_nl'] = nl_hypothesis
        true_label = judgment_dict[datapoint[columns[2]]]
        dat_temp_dict['label'] = true_label

        #Get nl_premise, hypothesis and not(hypothesis) fol string representation
        fol_premise = translation_dict[nl_premise]
        fol_premise = preprocessing.fol2nltk(fol_premise)
        dat_temp_dict['p_fol'] = fol_premise
        fol_hypothesis = translation_dict[nl_hypothesis]
        fol_hypothesis = preprocessing.fol2nltk(fol_hypothesis)
        fol_not_hypothesis = negated(fol_hypothesis)
        dat_temp_dict['h_fol'] = fol_hypothesis
        try:
            dat_temp_dict['e_pred'] = prover9_prove(PROVER9_BIN, fol_hypothesis, [fol_premise])
            dat_temp_dict['c_pred'] = prover9_prove(PROVER9_BIN, fol_not_hypothesis, [fol_premise])
            df.loc[len(df)] = dat_temp_dict
        except Exception as a:
            e_df.loc[len(e_df)] = {'nl_p':nl_premise,'nl_h':nl_hypothesis,'exception':str(a)}

    if not os.path.isdir("evaluations"):        
        os.mkdir("evaluations")
    df.to_csv(f"evaluations/{dataset_name}_evaluation.csv")
    e_df.to_csv(f"evaluations/{dataset_name}_exceptions.csv")

evaluate(sick_,fracas_dataset,['premise','hypothesis','label'],{0:"e",1:"n",2:"c"},"fracas")