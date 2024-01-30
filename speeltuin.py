from datasets import load_dataset 
import pandas as pd
import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove
import os 
import math

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

fracas_df = pd.read_csv("./datasets/fracas/fracas_full.csv",sep="\t")

temp_df = pd.DataFrame({"premises":[],"h":[],"label":[]})

# print(df_fracas.iloc[2]['premise'])

# def split_premises(s):
#     '''
#     Splits premises and returns them in the right format:
#     with a seperator " ## " in between.
#     '''
#     s_list = s.split(". ")
#     res = s_list[0]

#     for i in range(len(s_list))[1:]:
#         res = res + ". ## " + s_list[i]
    
#     print(res)

# split_premises(df_fracas.iloc[17]['premise'])

# # Quantifier set 1-80
# for i in range(80):
#     df.loc[len(df.id)] = {'premises':df_fracas.iloc[i],}

# Plural set 81 - 113

# Anaphora set 114 - 141

# Ellipsis set 142 - 196

# Adjectives 197 - 219

# Comparatives 220 - 250

# Temporal 251 - 325

# Attitudes 334 - 346

