import json, uuid, sys, re, os
import unicodedata
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from collections import OrderedDict

class PreProcess:
    """ This program aims to preprocess Train_en_new.json in new_dataset """
    """ python version == 3.7 """

    def __init__(self):
        self.src = sys.argv[1]
        self.dst = "new_dataset/"
        self.filename = "clean_train_data.json"

        self.text, self.begin, self.end = [],[],[]
        self.verbose = 1

    def get_data(self):
        print("Loading data from: " + "\033[1m" + sys.argv[1] + "\033[0m")

        with open(self.src) as f:
            data = json.load(f)

        self.text = data["text"]
        self.begin = data["begin_sentence"]
        self.end = data["end_sentence"]

        print("Loading data complete")

    def organize_sentences(self):
        print("Splitting sentences from raw text in data ...")

        words = self.text.split(" ")
        sentences = []
        for b, e in zip(self.begin, self.end):
            word_list = words[b:e]
            sentence = " ".join(word_list)
            self.clean_text(sentence)

            #print sentence
            sentences.append(sentence)

        return sentences
    
    def get_tokenized_sentences(self):
        print("Tokenizing sentences with NLTK ...")
        
        clean_text = self.clean_text(self.text)
        #custom_sent_tokenizer = PunktSentenceTokenizer(clean_text)
        #sent_tokenized_list = custom_sent_tokenizer.tokenize(clean_text)
        sent_tokenized_list = sent_tokenize(clean_text)

        #print("s1:", sent_tokenized_list1[2], "s2:", sent_tokenized_list2[2])
        return sent_tokenized_list

    def clean_text(self, text):

        text =re.sub(r'\s\d\s\.', ' ', text)
        text = re.sub(r"\\n(\d)", " ", text)
        #text = re.sub(r"\\n", " ",text)
        text = re.sub(r'\n', r' ', text)
        #text = re.sub(r"\'m", " am", s)
        # remove all punctuation
        #text = re.sub("([^\w\s]|\_)",r' ', text)
        text = text.encode().decode('utf-8')
        # remove extra spaces
        clean_text = re.sub(r'(\s)+', r' ', text)

        #print(clean_text)
        return clean_text


    def render(self, sentences, nltk_sentences):
        """ put things in order and render json file """

        print("Writing data to: " + str(self.dst) + "\033[1m" + str(self.filename) + "\033[0m")

        ordered_dict = OrderedDict()
        ordered_dict["begin"] = NoIndent(self.begin)
        ordered_dict["end"] = NoIndent(self.end)

        sentence_ordered_dict_list = []
        cnt = 0
        t_length = len(sentences)
        for s1, s2 in zip(sentences, nltk_sentences):
            cnt += 1
            sentence_ordered_dict = OrderedDict()
            sentence_ordered_dict["index"] = cnt
            sentence_ordered_dict["sentence"] = s1
            sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict))
            sentence_ordered_dict2 = OrderedDict()
            sentence_ordered_dict2["index"] = cnt
            sentence_ordered_dict2["nltk_sentence"] = s2
            sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict2))

            if self.verbose:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, t_length))
                sys.stdout.flush()

        ordered_dict["sentences"] = sentence_ordered_dict_list

        f = open(self.dst + "/" + self.filename, 'w+')
        f.write(json.dumps(ordered_dict, indent = 4, default=default))

class NoIndent(object):
    def __init__(self, value):
        self.value = value

def default(o, encoder=json.JSONEncoder()):
    if isinstance(o, NoIndent):
        return json.dumps(o.value)
    return encoder.default(o)

if __name__ == '__main__':
    preprocess = PreProcess()
    preprocess.get_data()
    sentences = preprocess.organize_sentences()
    nltk_sentences = preprocess.get_tokenized_sentences()
    preprocess.render(sentences, nltk_sentences)
