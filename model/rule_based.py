import spacy

class RuleBased:
    """ rule based approach with spacy """
    def __init__(self):
        pass

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