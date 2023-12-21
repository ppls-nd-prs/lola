def prepare_for_translation(dataset, columns: list):
  '''
  Prepares dataset for translation with simple_generate by 
  appending all dataset entries from the different columns
  and returning as one list.
  '''
  res = []
  for column in columns:
    res = res + dataset[column]
  return res

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
