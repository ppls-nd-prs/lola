import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing
from datasets import load_dataset, concatenate_datasets
import json
import nltk
import pandas as pd
import re
import os

#locate prover9
PROVER9_BIN = "./prover9/bin"
print(prover9_prove(PROVER9_BIN, "some y. man(y)", ["man(Alex)"]))

#load fracas
fracas = load_dataset("pietrolesci/fracas")
fracas_dataset = concatenate_datasets([fracas["train"],fracas["dev"]])

#get the dictionary
with open("dictionaries/fracas/full_fracas_dict.json","r") as file:
    fracas_dict = json.load(file)

# def evaluate_on_sick(translation_dict):
#     #0: entailment; 1: neutral; 2: contradiction
#     tp = 0; tn = 0; fp = 0; fn = 0
#     sick_data = load_dataset("sick", split="train")
#     for i,id in enumerate(sick_data['id'][:10]):
#         print(sick_data['sentence_A'][i])
#         sent_A = sick_data['sentence_A'][i]
#         print(sick_data['sentence_B'][i])
#         sent_B = sick_data['sentence_B'][i]
#         print(sick_data['label'][i])
#         fol_sent_A = preprocessing.fol2nltk(translation_dict[sent_A])
#         print(fol_sent_A)
#         fol_sent_B = preprocessing.fol2nltk(translation_dict[sent_B])
#         print(fol_sent_B)
#         try:
#             label = prover9_prove(PROVER9_BIN, fol_sent_A, [fol_sent_B])
#         except:
#             label = False
#         print(label)
#         sick_label = sick_data['label'][i]
#         if label == True and sick_label == 0:
#             tp += 1
#         elif label == True and (sick_label == 1 or sick_label == 2):
#             fp += 1
#         elif label == False and (sick_label == 0):
#             fn += 1
#         elif label == False and (sick_label == 1 or sick_label == 2):
#             tn += 1
        
#     return {"tp":tp,"fp":fp,"tn":tn,"fn":fn}

# print(evaluate_on_sick(sample_dict))

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

evaluate(fracas_dict,fracas_dataset,['premise','hypothesis','label'],{0:"e",1:"n",2:"c"},"fracas")