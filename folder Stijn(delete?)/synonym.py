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

    # Check for similarity based on WordNet paths and print 10 examples
    for i, syn1 in enumerate(synsets1):
        for j, syn2 in enumerate(synsets2):
            path_similarity = syn1.path_similarity(syn2)
            if path_similarity is not None:
                words1 = ", ".join(lemma.name() for lemma in syn1.lemmas())
                words2 = ", ".join(lemma.name() for lemma in syn2.lemmas())
                #print(f"Path Similarity {i+1}-{j+1}: {path_similarity:.4f}")
                #print(f"Words {i+1}: {words1}")
                #print(f"Words {j+1}: {words2}")
                #print()

    return False

# Example usage:
word5 = 'couch'
word6 = 'lounge'
result = are_synonyms(word5, word6)

print(f"Are '{word5}' and '{word6}' synonyms? {result}")
