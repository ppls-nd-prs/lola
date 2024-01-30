import pandas as pd

df_fracas = pd.read_csv("fracas_full.csv",sep='\t')
df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})

# Quantifier set 1-80
for i in range(len(df_fracas.index)):
    row = df_fracas.iloc[i]
    df_res.loc[len(df_res.index)] = {'id':row['_id'],'premises':row['premises'],'h':row['h'],'label':row['label']}
    if row['_id'] == 80:
        df_res.to_csv("01-fracas_quantifier_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 113:
        df_res.to_csv("02-fracas_plural_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 141:
        df_res.to_csv("03-fracas_anaphora_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 196:
        df_res.to_csv("04-fracas_ellipsis_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 219:
        df_res.to_csv("05-fracas_adjectives_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 250:
        df_res.to_csv("06-fracas_comparatives_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 325:
        df_res.to_csv("07-fracas_temporal_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 333:
        df_res.to_csv("08-fracas_verbs_set.csv",sep="\t")
        df_res = pd.DataFrame({'id':[],'premises':[],'h':[],'label':[]})
    elif row['_id'] == 346:
        df_res.to_csv("09-fracas_comparatives_set.csv",sep="\t")


# Adjectives 197 - 219

# Comparatives 220 - 250

# Temporal 251 - 325

# Attitudes 334 - 346
