import json
import os 

d = {}

directory = "dictionaries/sick"
out_filename = "dictionaries/sick/full_sick_dictionary.json"

print(os.listdir(directory))

for filename in os.listdir(directory):
    print("file name: ", filename)
    with open(directory + "/" + filename,"r") as file:
        new_d = json.load(file)
        d.update(new_d)

with open(out_filename,"w") as file:
    json.dump(d,file)