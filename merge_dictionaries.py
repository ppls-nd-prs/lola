import json

d = {}

for i in [100,200,300,400,500,600]:
    with open(f"dictionaries/fracas/fracas_dict_tm_{i}.json") as file:
        new_d = json.load(file)
        d.update(new_d)

with open("dictionaries/fracas/full_fracas_dict.json",'w') as file:
    json.dump(d,file)