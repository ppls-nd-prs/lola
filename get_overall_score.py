import os 
import pandas as pd

def get_scores(file_path : str):

    df = pd.read_csv(file_path,sep='\t',index_col=[0], header=[0])
    n_correct = df.iat[0,0] + df.iat[1,1] + df.iat[2,2]
    total = df.sum().sum()
    per_correct = n_correct / total

    scores = {"correctly classified" : per_correct}

    return scores

scores = pd.DataFrame()

#Get all relevant evaluation files 
for f in os.listdir("evaluations"):
    if "metrics" in f and not("train" in f or "trial" in f):   #get relevant files 
        name = f.replace("-[metrics].csv","") #get relevant file info 
        path = os.path.join("evaluations", f)
        scores[name] = get_scores(path)

for f in os.listdir("mod_evaluations"):
    if "metrics" in f and not("train" in f or "trial" in f):   #get relevant files 
        name = f.replace("-[metrics].csv","") #get relevant file info 
        path = os.path.join("mod_evaluations", f)
        scores[name] = get_scores(path)

scores = scores.T

scores.to_csv('overall_scores.csv',sep='\t')

