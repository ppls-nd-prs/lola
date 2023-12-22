import numpy as np

def prepare_for_translation(dataset, columns: list):
  '''
  Prepares dataset for translation with simple_generate by 
  appending all dataset entries from the different columns
  and returning as one numpy-array.
  '''
  res = []
  for column in columns:
    res = res + dataset[column]
  return np.array(res)

def generate_translation_dict(nl_dataset, FOL_generator):
  '''
  Generates translation dictionary with for {"nl_sentence":"fol_translation"}.
  Params:
  	- nl_dataset: list of nl sentences
  	- FOL_generator: logicllama translator from nl to fol
  '''
  translation_dict = {}
  for i in nl_dataset:
    translation_dict[i] = FOL_generator(input_str={"NL":i})[1][1]
  return translation_dict

def generate_samples_dict(prepared_dataset, n, generator):
  '''
  Generates a dictionary with as keys n samples selected from
  the prepared_dataset with as value their translation using generator.
  '''
  np.random.shuffle(prepared_dataset)
  data = prepared_dataset[:n]
  return generate_translation_dict(data,generator)
