from datasets import load_dataset 
import pandas as pd
import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove

PROVER9_BIN = "./prover9/bin"
prover9_prove(PROVER9_BIN, 'all x. man(x)', ['all x. thing(x)','all x. thing(x) -> man(x)'])

pass
fracas = load_dataset("pietrolesci/fracas")

df1 = pd.DataFrame(fracas['dev'])
print(df1.columns)
df2 = pd.DataFrame(fracas['train'])
df3 = pd.concat([df1,df2])
print(df3)

df = pd.DataFrame({"id":[],"p1":[],"p2":[],"p3":[],"h":[],"label":[]})

# for i in range(80):
#     df.loc[len(df.id)] = 

