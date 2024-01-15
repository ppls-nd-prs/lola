import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
from prepocessing import preprocessing
from datasets import load_dataset, concatenate_datasets
import json
import nltk

#locate prover9
PROVER9_BIN = "./prover9/bin"
print(prover9_prove(PROVER9_BIN, "some y. man(y)", ["man(Alex)"]))

#load fracas
fracas = load_dataset("pietrolesci/fracas")
fracas_dataset = concatenate_datasets([fracas["train"],fracas["dev"]])

print(fracas_dataset)

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

print(negated("all x. man(x)"))

def evaluate(translation_dict,dataset,columns,judgment_dict):
    '''
    columns should have format [premise-column-name,hypothesis-column-name,
    label-column-name]
    judgment_dict should have format {[value]:"entailment", [value]:"neutral",
    [value]:"contradiction"}
    '''
    #TODO: i) test for contradiction by checking for entailment of not(hypothesis),
    # ii) 
    #0: entailment; 1: neutral; 2: contradiction
    ee = 0; en = 0; ec = 0; ne = 0; nn = 0; nc = 0; ce = 0; cn = 0; cc = 0
    syntactically_wrong = 0
    for datapoint in dataset:
        print('***')
        print(datapoint)
        print(datapoint[columns[0]])
        print("***")
        premise = datapoint[columns[0]]
        hypothesis = datapoint[columns[1]]
        true_label = judgment_dict[datapoint[columns[2]]]
        print(true_label)
        fol_premise = preprocessing.fol2nltk(translation_dict[premise])
        print("not fol_premise: ", negated(fol_premise))
        fol_hypothesis = preprocessing.fol2nltk(translation_dict[hypothesis])
        try:
            direct_pred_label = prover9_prove(PROVER9_BIN, fol_premise, [fol_hypothesis])
        except:
            syntactically_wrong += 1
        if true_label == "entailment":
            if pred_label == True:
                ee += 1
        elif label == True and (label == 1 or label == 2):
            fp += 1
        elif label == False and (label == 0):
            fn += 1
        elif label == False and (label == 1 or label == 2):
            tn += 1
        
    return {"tp":tp,"fp":fp,"tn":tn,"fn":fn,"sw":syntactically_wrong}



# print(evaluate(fracas_dict,fracas_dataset,['premise','hypothesis','label'],{0:"entailment",1:"neutral",2:"contradiction"}))