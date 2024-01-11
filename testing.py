import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing


PROVER9_BIN = "./prover9/bin"
print(prover9_prove(PROVER9_BIN, "some y. man(y)", ["man(Alex)"]))

from datasets import load_dataset
import json

with open("sick_dict_tm_100.json","r") as file:
    sample_dict = json.load(file)

def evaluate_on_sick(translation_dict):
    #0: entailment; 1: neutral; 2: contradiction
    sick_data = load_dataset("sick", split="train")
    for i,id in enumerate(sick_data['id'][:10]):
        print(sick_data['sentence_A'][i])
        sent_A = sick_data['sentence_A'][i]
        print(sick_data['sentence_A'][i])
        sent_B = sick_data['sentence_A'][i]
        print(sick_data['label'][i])
        fol_sent_A = preprocessing.fol2nltk(translation_dict[sent_A])
        print(fol_sent_A)
        fol_sent_B = preprocessing.fol2nltk(translation_dict[sent_B])
        print(fol_sent_B)
        label = prover9_prove(PROVER9_BIN, fol_sent_A, [fol_sent_B])
        print(label)

evaluate_on_sick(sample_dict)