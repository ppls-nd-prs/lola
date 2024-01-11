import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing
from datasets import load_dataset
import json

#locate prover9
PROVER9_BIN = "./prover9/bin"
print(prover9_prove(PROVER9_BIN, "some y. man(y)", ["man(Alex)"]))

#get the dictionary
with open("sick_dict_first_10_samples.json","r") as file:
    sample_dict = json.load(file)

def evaluate_on_sick(translation_dict):
    #0: entailment; 1: neutral; 2: contradiction
    tp = 0; tn = 0; fp = 0; fn = 0
    sick_data = load_dataset("sick", split="train")
    for i,id in enumerate(sick_data['id'][:10]):
        print(sick_data['sentence_A'][i])
        sent_A = sick_data['sentence_A'][i]
        print(sick_data['sentence_B'][i])
        sent_B = sick_data['sentence_B'][i]
        print(sick_data['label'][i])
        fol_sent_A = preprocessing.fol2nltk(translation_dict[sent_A])
        print(fol_sent_A)
        fol_sent_B = preprocessing.fol2nltk(translation_dict[sent_B])
        print(fol_sent_B)
        try:
            label = prover9_prove(PROVER9_BIN, fol_sent_A, [fol_sent_B])
        except:
            label = False
        print(label)
        sick_label = sick_data['label'][i]
        if label == True and sick_label == 0:
            tp += 1
        elif label == True and (sick_label == 1 or sick_label == 2):
            fp += 1
        elif label == False and (sick_label == 0):
            fn += 1
        elif label == False and (sick_label == 1 or sick_label == 2):
            tn += 1
        
    return {"tp":tp,"fp":fp,"tn":tn,"fn":fn}

print(evaluate_on_sick(sample_dict))