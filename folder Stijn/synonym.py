import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def are_synonyms(word1, word2):
    # Get synsets for both words
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    # Check if there is any common synset between the two words
    common_synsets = set(synsets1).intersection(synsets2)

    if common_synsets:
        return True

    # Check for similarity based on WordNet paths
    for syn1 in synsets1:
        for syn2 in synsets2:
            path_similarity = syn1.path_similarity(syn2)
            if path_similarity is not None and path_similarity > 0.4:
                return True

    return False

# Example usage:
word5 = 'couch'
word6 = 'bench'
result = are_synonyms(word5, word6)

print(f"Are '{word5}' and '{word6}' synonyms? {result}")
