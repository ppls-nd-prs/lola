import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing
import json
import nltk
import pandas as pd
import re
import os
from data_transformations import prepare_for_translation
import argparse

def negated(fol_string):
    return "not " + fol_string


import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn


def are_synonyms(word1, word2):
    # Get synsets for both words
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    # Check if there is any common synset between the two words
    common_synsets = set(synsets1).intersection(synsets2)

    if common_synsets:
        return True

    # Check for similarity based on WordNet paths and print 10 examples
    for i, syn1 in enumerate(synsets1):
        for j, syn2 in enumerate(synsets2):
            path_similarity = syn1.path_similarity(syn2)
            if path_similarity is not None:
                words1 = ", ".join(lemma.name() for lemma in syn1.lemmas())
                words2 = ", ".join(lemma.name() for lemma in syn2.lemmas())
                #print(f"Path Similarity {i+1}-{j+1}: {path_similarity:.4f}")
                #print(f"Words {i+1}: {words1}")
                #print(f"Words {j+1}: {words2}")
                #print()

    return False

# Example usage:
word5 = 'couch'
word6 = 'lounge'
result = are_synonyms(word5, word6)

print(f"Are '{word5}' and '{word6}' synonyms? {result}")


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

        nl_hypothesis = dataset[columns[1]][i_dat]
        dat_temp_dict['h_nl'] = nl_hypothesis
        true_label = judgment_dict[dataset[columns[2]][i_dat]]
        dat_temp_dict['label'] = true_label

        # Get nl_premise, hypothesis and not(hypothesis) fol string representation
        fol_hypothesis = translation_dict[nl_hypothesis]
        fol_hypothesis = preprocessing.fol2nltk(fol_hypothesis)
        fol_not_hypothesis = negated(fol_hypothesis)
        dat_temp_dict['h_fol'] = fol_hypothesis
        
        # Check for synonyms between any word in premises and hypothesis
        found_synonym = False
        for prem_i, prem_col in enumerate(columns[0]):
            nl_premise = dataset[prem_col][i_dat]
            if are_synonyms(nl_premise, nl_hypothesis):
                print(f"Synonym relation found: {nl_premise} <-> {nl_hypothesis}")
                # Adjust label prediction accordingly
                dat_temp_dict['e_pred'] = 'e'  # Set label to entailment
                dat_temp_dict['c_pred'] = 'n'  # Set label to neutral (or adjust as needed)
                found_synonym = True
                break  # Break the loop if a synonym relation is found

        # Perform the prover9_prove if no synonym relation was found
        if not found_synonym:
            try:
                dat_temp_dict['e_pred'] = prover9_prove(PROVER9_BIN, fol_hypothesis, prover_premise_list)
                dat_temp_dict['c_pred'] = prover9_prove(PROVER9_BIN, negated(fol_hypothesis), prover_premise_list)
                df.loc[len(df)] = dat_temp_dict
            except Exception as a:
                dat_temp_dict['exception'] = str(a)
                e_df.loc[len(e_df)] = dat_temp_dict
            
    if not os.path.isdir("evaluations_SYN"):        
        os.mkdir("evaluations_SYN")
    df.to_csv(f"evaluations_SYN/{csv_name}_evaluation_SYN.csv",sep='\t')
    e_df.to_csv(f"evaluations_SYN/{csv_name}_exceptions_SYN.csv",sep='\t')
    
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
