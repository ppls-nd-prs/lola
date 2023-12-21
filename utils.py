def prepare_for_translation(dataset, columns: list):
  res = []
  for column in columns:
    res = res + dataset[column]
  return res

def generate_translation_dict(nl_dataset, FOL_generator: partial):
  translation_dict = {}
  for i in nl_dataset:
    translation_dict[i] = FOL_generator(input_str={"NL":i})[1][1]
  return translation_dict
