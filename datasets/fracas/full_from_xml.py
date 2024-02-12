import pandas as pd

in_df = pd.read_csv("fracas_from_xml.csv",sep=",")
out_df = pd.DataFrame({'_id':[],'premises':[],'h':[],'label':[]})
print("df_fracas: ", in_df.head())
for i in range(len(in_df)):
    row = in_df.iloc[i]
    res = row['p1']
    for j in [2,3,4,5]:
        if type(row[f'p{j}']) == str:
            res = res + " ## " + row[f'p{j}']
    if type(row['h']) == str:
        out_df.loc[len(out_df)] = {'_id':row['_id'],'premises':res,'h':row['h'],'label':row['label']}

print(out_df)

out_df.to_csv("fracas-full.csv",sep="\t")
