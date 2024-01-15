import nltk 

def proof_9(conclusion : nltk.sem.Expression, premises :[nltk.sem.Expression]):
    prover9 = nltk.Prover9()
    prover9.config_prover9("./prover9/bin")
    try:
        return prover9.prove(conclusion, premises) 
    except OSError as e:
        raise OSError(f"{e}. Try running this in Google Colab") from None #prover9 exec needs linux 