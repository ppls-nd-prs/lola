import pandas as pd
from data_transformations import prepare_for_translation

sick = pd.read_csv("datasets/sick/SICK_test_annotated.csv",sep="\t")

sick_prepared = prepare_for_translation(sick,["sentence_A","sentence_B"])

print(sick["sentence_A"][:2],end="\n\n")
print(sick["sentence_B"][:2],end="\n\n")
print(len(sick["sentence_A"]))
print(len(sick_prepared))
