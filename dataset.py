import re, json

class TextDataset:
    def __init__(self, src):
        #self.data = self.get_train(src)
        self.data = self.load_train_en(src)

        self.text = self.data["text"].replace("\n","")
        self.tokenized_corpus = self.text.split(" ")
        self.begin = self.data["begin_sentence"]
        self.end = self.data["end_sentence"]
    
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

    # def get_ground_truth(self):

    #     """ get ground truth """
    #     print("Getting ground truth ...")

    #     # Splitting sentences from raw text in corpus
    #     ground_truth = []
    #     for b, e in zip(self.begin, self.end):
    #         # add 1 to include the last index
    #         words = self.tokenized_corpus[b:e+1]
    #         sentence = " ".join(words)

    #         index = [b,e]
    #         # grouth_truth = [ [[22, 29], [blah blah ... blah"], * n ]
    #         ground_truth.append([index, sentence])

    #     return ground_truth
    
    # def get_nltk_result(self):
    #     """ get nltk result | the format is the same as ground truth """
    #     print("Getting nltk result ... ")
        
    #     # tokenizing sentences with NLTK
    #     tokenized_sentences = sent_tokenize(self.text)
    #     tokenized_words = [s.split(" ") for s in tokenized_sentences]

    #     # get tokenized_sentence index
    #     result, sentences, begin, end = [], [], [], []
    #     for words in tqdm(tokenized_words):

    #         sentence_index, tarket_words = self.find_sublist_index(words, self.tokenized_corpus)
    #         sentence = " ".join(tarket_words)

    #         # filter out sentences if it is too short
    #         if int(sentence_index[1]) - int(sentence_index[0]) >= 5:
    #             #sentence = self.clean_text(sentence)
    #             sentences.append([sentence_index, sentence])
    #             begin.append(sentence_index[0])
    #             end.append(sentence_index[1])
    #         else:
    #             pass

    #     evaluation = self.evaluate(begin, end)
    #     result = {"begin":begin, "end":end, "sentences":sentences, "evaluation":evaluation}

    #     return result