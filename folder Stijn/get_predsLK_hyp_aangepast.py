import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

import sys
sys.path.insert(1, '/content/lola')
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
import argparse

def negated(fol_string):
    return "not " + fol_string

def has_hyponym_hypernym_relation(word1, word2):
    # Check if there is a hyponym/hypernym relation between two words based on WordNet.
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    for syn1 in synsets1:
        for syn2 in synsets2:
            if syn1 in syn2.lowest_common_hypernyms(syn1):
                return True
            elif syn2 in syn1.lowest_common_hypernyms(syn2):
                return True

    return False

def get_preds_with_lexical(translation_dict, dataset, columns, judgment_dict, csv_name: str):
    # Initialize empty DataFrames
    df_columns = ['p_1_nl', 'p_1_fol', 'p_2_nl', 'p_2_fol', 'h_nl', 'h_fol', 'label', 'e_pred', 'c_pred']
    df = pd.DataFrame(columns=df_columns)
    
    e_df_columns = ['p_1_nl', 'p_1_fol', 'p_2_nl', 'p_2_fol', 'h_nl', 'h_fol', 'label', 'exception']
    e_df = pd.DataFrame(columns=e_df_columns)

    for i_dat in range(len(dataset)):
        print("progress: " + str(int(i_dat/len(dataset)*100)) + "%", end='\r')
        dat_temp_dict = {}
        prover_premise_list = []

        # get premises and hypothesis natural string representation
        for prem_i, prem_col in enumerate(columns[0]):
            nl_premise = dataset[prem_col][i_dat]
            dat_temp_dict[f'p_{prem_i+1}_nl'] = nl_premise
            fol_premise = translation_dict[nl_premise]
            fol_premise = preprocessing.fol2nltk(fol_premise)
            prover_premise_list.append(fol_premise)
            dat_temp_dict[f'p_{prem_i+1}_fol'] = fol_premise

            # Check for hyponym/hypernym relation between words in the premise
            if prem_i > 0:
                prev_nl_premise = dataset[columns[0][prem_i - 1]][i_dat]
                if has_hyponym_hypernym_relation(nl_premise, prev_nl_premise):
                    print(f"Hyponym/Hypernym relation found: {nl_premise} <-> {prev_nl_premise}")
                    # Adjust label prediction accordingly
                    dat_temp_dict['e_pred'] = 'e'  # Set label to entailment
                    dat_temp_dict['c_pred'] = 'n'  # Set label to neutral (or adjust as needed)
                    continue  # Skip further processing for this example

        nl_hypothesis = dataset[columns[1]][i_dat]
        dat_temp_dict['h_nl'] = nl_hypothesis
        true_label = judgment_dict[dataset[columns[2]][i_dat]]
        dat_temp_dict['label'] = true_label

        # Get nl_premise, hypothesis and not(hypothesis) fol string representation
        fol_hypothesis = translation_dict[nl_hypothesis]
        fol_hypothesis = preprocessing.fol2nltk(fol_hypothesis)
        fol_not_hypothesis = negated(fol_hypothesis)
        dat_temp_dict['h_fol'] = fol_hypothesis

        # Check for hyponym/hypernym relation between words in the hypothesis
        if has_hyponym_hypernym_relation(nl_hypothesis, dataset[columns[0][-1]][i_dat]):
            print(f"Hyponym/Hypernym relation found: {nl_hypothesis} <-> {dataset[columns[0][-1]][i_dat]}")
            # Adjust label prediction accordingly
            dat_temp_dict['e_pred'] = 'e'  # Set label to entailment
            dat_temp_dict['c_pred'] = 'n'  # Set label to neutral (or adjust as needed)
            continue  # Skip further processing for this example

        try:
            # Only perform the prover9_prove if hyponym/hypernym relation was not found
            if 'e_pred' not in dat_temp_dict:
                dat_temp_dict['e_pred'] = prover9_prove(PROVER9_BIN, fol_hypothesis, prover_premise_list)
            if 'c_pred' not in dat_temp_dict:
                dat_temp_dict['c_pred'] = prover9_prove(PROVER9_BIN, negated(fol_hypothesis), prover_premise_list)
            df.loc[len(df)] = dat_temp_dict
        except Exception as a:
            dat_temp_dict['exception'] = str(a)
            e_df.loc[len(e_df)] = dat_temp_dict
            
    if not os.path.isdir("evaluations_stijn2"):        
        os.mkdir("evaluations_stijn2")
    df.to_csv(f"evaluations_stijn2/{csv_name}_evaluation_stijn2.csv",sep='\t')
    e_df.to_csv(f"evaluations_stijn2/{csv_name}_exceptions_stijn2.csv",sep='\t')
    
    #get dataset information
parser = argparse.ArgumentParser()
parser.add_argument('dataset_name',choices=['sick_trial','sick_train','sick_test','syllogisms'],help='dataset_name')
args = parser.parse_args()
dataset_name = args.dataset_name  

if re.search(r'sick',dataset_name):
    dictionary_path = "dictionaries/sick/full_sick_dictionary.json"
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
    dictionary_path = "dictionaries/syllogisms/syllogism_dict.json"
    relevant_column_list = [['prem_1','prem_2'],'hypothesis','label']
    judgment_dict = {"entailment":"e","neutral":"n","contradiction":"c"}
    
#locate prover9
PROVER9_BIN = "./prover9/bin"

#load dataslet
dataset = pd.read_csv(dataset_path,header=0,sep="\t")

#get the dictionary
with open(dictionary_path,"r") as file:
    dictionary = json.load(file)



# Example usage
    get_preds_with_lexical(dictionary, dataset, relevant_column_list, judgment_dict, dataset_name)
