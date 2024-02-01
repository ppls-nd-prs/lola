import pandas as pd
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('file_path',help='file_path')
args = parser.parse_args()
file_path = args.file_path

eval_df = pd.read_csv(file_path,sep='\t')

table = {"classified as e":[],"classified as c":[],"classified as n":[],"classified as both":[]}

# Fill class_as_e
class_as_e = []
for i,gold in enumerate(['e','c','n']):
    sub_df = eval_df[eval_df['label'] == gold]
    sub_df = sub_df[sub_df['e_pred'] == True]
    sub_df = sub_df[sub_df['c_pred'] == False]
    class_as_e.append(len(sub_df))
table['classified as e'] = class_as_e

# Fill class_as_c
class_as_c = []
for i,gold in enumerate(['e','c','n']):
    sub_df = eval_df[eval_df['label'] == gold]
    sub_df = sub_df[sub_df['e_pred'] == False]
    sub_df = sub_df[sub_df['c_pred'] == True]
    class_as_c.append(len(sub_df))
table['classified as c'] = class_as_c

# Fill class_as_n
class_as_n = []
for i,gold in enumerate(['e','c','n']):
    sub_df = eval_df[eval_df['label'] == gold]
    sub_df = sub_df[sub_df['e_pred'] == False]
    sub_df = sub_df[sub_df['c_pred'] == False]
    class_as_n.append(len(sub_df))
table['classified as n'] = class_as_n

# Fill class_as_both
class_as_both = []
for i,gold in enumerate(['e','c','n']):
    sub_df = eval_df[eval_df['label'] == gold]
    sub_df = sub_df[sub_df['e_pred'] == True]
    sub_df = sub_df[sub_df['c_pred'] == True]
    class_as_both.append(len(sub_df))
table['classified as both'] = class_as_both

df = pd.DataFrame(table)
df.to_csv(f'{file_path[:-4]}-[metrics].csv',sep='\t')

