import re, json

class TextDataset:
    """ load data from paths.json | preprocess """
    def __init__(self, src):
        self.raw_data = self.load_train_en(src)

        self.text = self.raw_data['text'].replace("\n","")
        #print(self.text[157:1239])
        self.clean_text = self.get_clean_text(self.text).strip()

        self.tokens = self.text.split(" ")
        self.idx_tokens = self.get_indexed_tokens()
        self.clean_idx_tokens = self.get_clean_tokens(self.idx_tokens)
        
        l = self.clean_text.split(" ")

        self.begin = self.raw_data['begin_sentence']
        self.end = self.raw_data['end_sentence']

        self.ground_truth = self.get_ground_truth(self.begin, self.end, self.clean_idx_tokens)
    
    def __len__(self):
        return len(self.tokens)
    
    def get_indexed_tokens(self):
        """ [[0, 'word1'], [1, 'word2'], [2, 'word3'], ..., [n-1, 'wordn'] """
        return [[i, word] for i, word in enumerate(self.tokens)]

    def get_clean_text(self, text):
        """ remove noise """
        text = re.sub('[0-9]+', '', text)
        text = re.sub('\s+', ' ', text)
        
        #remove unnecessary full stop
        text = re.sub('(\.\s)+', '. ', text)
        return text

    def get_clean_tokens(self, tokens):
        """ remove noise """
        clean = []
        #regex = re.compile('[0-9]+')
        for idx_tok in tokens:
            idx_tok[1] = re.sub('[0-9]+', '', idx_tok[1])
            if idx_tok[1] == "":
                pass
            else:
                clean.append(idx_tok)

        i = 0
        while i < len(clean)-1:
            if clean[i][1] == clean[i+1][1] and clean[i+1][1] == ".":
                del clean[i+1]
            else:
                i = i+1        
        #print(clean)
        return clean

    def get_ground_truth(self, begin, end, tokens):
        """ get ground truth """
        print("Getting ground truth ...")

        ground_truth = []
        # Splitting sentences from raw text in corpus
        for b, e in zip(begin, end):

            boundary = 0
            flag = 0
            sentence = []
            for token in tokens:
                boundary += 1
                if token[0] == e:
                    sentence.append(token)
                    flag = 0
                    break
                elif token[0] == b or flag == 1:
                    sentence.append(token)
                    flag = 1
                else:
                    flag = 0
                    pass

            tokens = tokens[boundary:]
            ground_truth.append(sentence)

        return ground_truth
    
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
