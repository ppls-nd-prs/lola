from datasets import load_dataset 
import pandas as pd
import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
import os 

#TODO: loop over all instances in the fracas dataset and
#save them under the right type of inference
#seperate premises w/ " ## " and
#save the resulting dataframe in 'fracas.csv'

# df = pd.read_csv('./datasets/syllogisms/syllogisms_old.csv',sep="\t")

# df['premises'] = df['prem_1'] + " ## " + df['prem_2']

# df = df.drop(['prem_1','prem_2'],axis=1)

# df.to_csv("./datasets/syllogisms/syllogisms.csv",sep="\t")

# PROVER9_BIN = "./prover9/bin"
# label = prover9_prove(PROVER9_BIN, 'all x. man(x)', ['all x. thing(x)','all x. thing(x) -> man(x)',''])
# print(label)

fracas = load_dataset("pietrolesci/fracas")

df1 = pd.DataFrame(fracas['dev'])
print(df1.columns)
df2 = pd.DataFrame(fracas['train'])
df3 = pd.concat([df1,df2])
print(df3)

df = pd.DataFrame({"id":[],"p1":[],"p2":[],"p3":[],"h":[],"label":[]})

# for i in range(80):
#     df.loc[len(df.id)] = 

