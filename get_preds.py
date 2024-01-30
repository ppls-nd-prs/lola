import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing
# from datasets import load_dataset, concatenate_datasets
import json
import nltk
import pandas as pd
import re
import os
from data_transformations import prepare_for_translation
import argparse

def negated(fol_string):
    return "not " + fol_string

def get_preds(translation_dict,dataset,columns,judgment_dict,csv_name: str, modification_id :str):
    '''
    columns should have format [[premise-1-column-name,premise-2-column-name,etc.],
    hypothesis-column-name, label-column-name]
    judgment_dict should have format {[value]:"e", [value]:"n",
    [value]:"c"}.
    modification_id indicates the modification used
    Returns a pandas dataframe with premises, hypothesis, e_pred and c_pred
    '''
    nr_premises = len(columns[0])
    start_d = {}
    for i in range(nr_premises):
        start_d[f'p_{i+1}_nl'] = []
        start_d[f'p_{i+1}_fol'] = []
    start_d.update({'h_nl':[],'h_fol':[],'label':[]})
    start_d['exception'] = []
    e_df = pd.DataFrame(start_d)
    del start_d['exception']
    start_d.update({'e_pred':[],'c_pred':[]})
    df = pd.DataFrame(start_d)
    for i_dat in range(len(dataset)):
        print("progress: " + str(int(i_dat/len(dataset)*100)) + "%", end='\r')
        dat_temp_dict = {}
        prover_premise_list = []
        # get premises and hypothesis natural string representation
        for prem_i,prem_col in enumerate(columns[0]):
            nl_premise = dataset[prem_col][i_dat]
            dat_temp_dict[f'p_{prem_i+1}_nl'] = nl_premise
            fol_premise = translation_dict[nl_premise]
            fol_premise = preprocessing.fol2nltk(fol_premise)
            prover_premise_list.append(fol_premise)
            dat_temp_dict[f'p_{prem_i+1}_fol'] = fol_premise
        nl_hypothesis = dataset[columns[1]][i_dat]
        dat_temp_dict['h_nl'] = nl_hypothesis
        true_label = judgment_dict[dataset[columns[2]][i_dat]]
        dat_temp_dict['label'] = true_label

        #Get nl_premise, hypothesis and not(hypothesis) fol string representation
        fol_hypothesis = translation_dict[nl_hypothesis]
        fol_hypothesis = preprocessing.fol2nltk(fol_hypothesis)
        fol_not_hypothesis = negated(fol_hypothesis)
        dat_temp_dict['h_fol'] = fol_hypothesis
        try:
            dat_temp_dict['e_pred'] = prover9_prove(PROVER9_BIN, fol_hypothesis, prover_premise_list)
            dat_temp_dict['c_pred'] = prover9_prove(PROVER9_BIN, fol_not_hypothesis, prover_premise_list)
            df.loc[len(df)] = dat_temp_dict
        except Exception as a:
            dat_temp_dict['exception'] = str(a)            
            e_df.loc[len(e_df)] = dat_temp_dict
    if modification_id == "none": #if there was no modification 
        if not os.path.isdir("evaluations"):        
            os.mkdir("evaluations")
        df.to_csv(f"evaluations/{csv_name}_evaluation.csv",sep='\t')
        e_df.to_csv(f"evaluations/{csv_name}_exceptions.csv",sep='\t')
    else:
        if not os.path.isdir("mod_evaluations"):        
            os.mkdir("mod_evaluations")
        df.to_csv(f"mod_evaluations/[{modification_id}]{csv_name}_evaluation.csv",sep='\t')    #just save the evaluations

#get dataset information
parser = argparse.ArgumentParser()
parser.add_argument('dataset_name',choices=['sick_trial','sick_train','sick_test','syllogisms'],help='dataset_name')
parser.add_argument('modification_id',choices=['a2e', 'i2c_a2e', 'none'],help='modification_id')   #possible to have no modification
args = parser.parse_args()
dataset_name = args.dataset_name  
modification_id = args.modification_id

if re.search(r'sick',dataset_name):
    if modification_id == "none": 
        dictionary_path = "dictionaries/sick/full_sick_dictionary.json"
    else:
        dictionary_path = f"mod_dictionaries/[{modification_id}]full_sick_dictionary.json"
    relevant_column_list = [['sentence_A'],'sentence_B','entailment_judgment']
    judgment_dict = {"ENTAILMENT":"e","NEUTRAL":"n","CONTRADICTION":"c"}
    if dataset_name == "sick_trial":
        dataset_path = "datasets/sick/SICK_trial.csv"
    elif dataset_name == "sick_train":
        dataset_path = "datasets/sick/SICK_train.csv"
    elif dataset_name == "sick_test":
        dataset_path = "datasets/sick/SICK_test_annotated.csv"
elif dataset_name == "syllogisms":
    dataset_path = "datasets/syllogisms/syllogisms.csv"
    if modification_id == "none": 
        dictionary_path = "dictionaries/syllogisms/syllogism_dict.json"
    else:
        raise(f"There are no modified dictionaries for the {dataset_name} data set")
    relevant_column_list = [['prem_1','prem_2'],'hypothesis','label']
    judgment_dict = {"entailment":"e","neutral":"n","contradiction":"c"}
# elif dataset_name == "fracas":
#     dataset_path = 
#TODO: extend for other datasets    

#locate prover9
PROVER9_BIN = "./prover9/bin"

#load dataset
dataset = pd.read_csv(dataset_path,header=0,sep="\t")

#get the dictionary
with open(dictionary_path,"r") as file:
    dictionary = json.load(file)

#get the predictions using the dictionary
get_preds(dictionary,dataset,relevant_column_list,judgment_dict,dataset_name,modification_id)
