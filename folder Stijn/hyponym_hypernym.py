#function to look if there are hypernym relations between words

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def has_hyponym_hypernym_relation(word1, word2):

    #Check if there is a hyponym/hypernym relation between two words based on WordNet.



    # Get synsets  for both words
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    # Check if word1 is a hyponym of word2 or vice versa
    for syn1 in synsets1:
        for syn2 in synsets2:
            if syn1 in syn2.lowest_common_hypernyms(syn1):
                return True
            elif syn2 in syn1.lowest_common_hypernyms(syn2):
                return True

    return False  # Return False if no hyponym/hypernym relationship is found

word3 = 'oak'
word4 = 'tree'
has_hyponym_hypernym_relation(word3,word4)
