import re, json

class TextDataset:
    """ load data from paths.json """
    def __init__(self, src):
        self.data = self.load_train_en(src)

        self.text = self.data['text'].replace("\n","")
        self.tokenized_corpus = self.text.split(" ")
        self.indexed_corpus = self.get_indexed_corpus()
        self.begin = self.data["begin_sentence"]
        self.end = self.data["end_sentence"]
    
    def __len__(self):
        return len(self.tokenized_corpus)
    
    def get_indexed_corpus(self):
        """ [[0, 'word1'], [1, 'word2'], [2, 'word3'], ..., [n-1, 'wordn'] """
        return [[i, word] for i, word in enumerate(self.tokenized_corpus)]
    
    def load_train_en(self, src):
        """ load English training set """
        with open('paths.json', 'r') as f:
            paths = json.load(f)
            return load_data(paths[src])

    def load_train_fr(self):
        """ load English training set """
        with open('paths.json', 'r') as f:
            paths = json.load(f)
            return load_data(paths['train_fr'])

    def load_test_en(self):
        """ load English testing set """
        with open('paths.json', 'r') as f:
            paths = json.load(f)
            return load_data(paths['test_en'])

    def load_test_fr(self):
        """ load English testing set """
        with open('paths.json', 'r') as f:
            paths = json.load(f)
            return load_data(paths['test_fr'])

def load_data(path):
    """ return json as a dict """
    with open(path, 'r') as f:
        return json.load(f)


    # def clean_text(self, text):
    #     """ customized clean text """
    # # remove unnecessary digits
    # text =re.sub(r'\s\d\s\.', '', text)
    # # remove all punctuation
    # #text = re.sub("([^\w\s]|\_)",r' ', text)
    # text = text.encode().decode('utf-8')
    # # remove extra spaces
    # clean_text = re.sub(r'(\s)+', r' ', text)

    # return clean_text
