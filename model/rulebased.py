import nltk, spacy
from nltk.tokenize import sent_tokenize

class RuleBased:
    """ rule based approach with spacy """
    def __init__(self):
        pass

    def get_nltk_tokenized_sentences(self, text):
        """
        tokenize sentence by NLTK 
        return a list of sentence -> ['sentence1', 'sentence2', ..., 'sentenceN']
        """
        #print("Getting nltk result ... ")
        tokenized_sentences = sent_tokenize(text)
        return tokenized_sentences

    def filter_subject(self, sentences):
        """ find sentences must have a nsubj(subject) and a root(verb) """
        nlp = spacy.load("en")

        #flag_tags = ["nsubj", "ROOT"]
        filtered_sentences = []

        for s in sentences:
            doc = nlp(s)
            
            if "nsubj" in [token.dep_ for token in doc]:
                filtered_sentences.append(doc.text)
                # print(doc.text)

        return filtered_sentences
    
    def filter_verb(self, sentences):
        nlp = spacy.load("en")

        #flag_tags = ["nsubj", "ROOT"]
        filtered_sentences = []

        for s in sentences:
            doc = nlp(s)
            
            if "ROOT" in [token.dep_ for token in doc]:
                filtered_sentences.append(doc.text)
                # print(doc.text)

        return filtered_sentences