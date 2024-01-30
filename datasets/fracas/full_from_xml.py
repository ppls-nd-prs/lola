import pandas as pd

df_fracas = pd.read_csv("fracas_from_xml.csv",sep=",")

print("df_fracas: ", df_fracas.head())
res_list = []
for i in range(len(df_fracas)):
    row = df_fracas.iloc[i]
    res = row['p1']
    for j in [2,3,4,5]:
        if type(row[f'p{j}']) == str:
            print(type(row[f'p{j}']))
            res = res + " ## " + row[f'p{j}']
    res_list.append(res)
df_fracas['premises'] = res_list

for i in [1,2,3,4,5]:
    df_fracas = df_fracas.drop(f"p{i}",axis=1)

print(df_fracas)

df_fracas.to_csv("fracas_full.csv",sep="\t")
