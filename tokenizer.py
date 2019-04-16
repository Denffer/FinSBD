
import nltk
from nltk.tokenize import sent_tokenize

class Tokenizer:
    """ tokenize sentence """

    def __init__(self):
        pass

    def text_tokenize(self, text):
        """ tokenize sentence by NLTK """
        return sent_tokenize(text)
    

