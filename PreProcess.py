import json, uuid, sys, re, os
import unicodedata
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from collections import OrderedDict
import nltk
import spacy

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
    
    def get_nltk_tokenized_sentences(self):
        print("Tokenizing sentences with NLTK ...")
        
        # clean_text is a long string
        clean_text = self.clean_text(self.text)
        tokenized_sentences = sent_tokenize(clean_text)

        # tokenize every sentence in tokenized_sentences 
        #pos_tagged_sentences = self.get_pos_tagged_sentences(tokenized_sentences)
        #self.filter_sentences(tokenized_sentences)

        return tokenized_sentences
    
    def get_spacy_tokenized_sentences(self):
        print("Tokenizing sentences with SpaCy ...")
        """ bad performance """

        clean_text = self.clean_text(self.text)

        # divide clean_text into sub_strings
        chunks, chunk_size = len(clean_text), int(len(clean_text)/5)
        sub_clean_text_list = [clean_text[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

        nlp = spacy.load("en")

        for text in sub_clean_text_list:
            doc = nlp(text)
            tokenized_sentences = [sent.string.strip() for sent in doc.sents]
        #print(tokenized_sentences)

        return tokenized_sentences
    
    # unused
    def get_pos_tagged_sentences(self, sentences):
        print("Pos-tagging the words in every sentence ...")

        for s in sentences:
            tokens = nltk.word_tokenize(s)
            pos_tagged_tokens = nltk.pos_tag(tokens)
            print(pos_tagged_tokens)
        
        return pos_tagged_tokens

    def get_filtered_sentences(self, sentences):
        """
        Filter sentences by using spacy
        A sentence must have a subject and a verb
        """
        # Load English tokenizer, tagger, parser, NER and word vectors
        nlp = spacy.load("en")

        #flag_tags = ["nsubj", "ROOT"]
        filtered_sentences = []

        for s in sentences:
            doc = nlp(s)
            #token_deps = [token.dep_ for token in doc]
            #print(token_deps)
            
            if "nsubj" in [token.dep_ for token in doc]:
                filtered_sentences.append(doc.text)
                # print(doc.text)



            

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


    def render(self, ground_truth_sentences, nltk_sentences, spacy_sentences):
        """ put things in order and render json file """

        print("Writing data to: " + str(self.dst) + "\033[1m" + str(self.filename) + "\033[0m")

        ordered_dict = OrderedDict()
        ordered_dict["begin"] = NoIndent(self.begin)
        ordered_dict["end"] = NoIndent(self.end)

        sentence_ordered_dict_list = []
        cnt = 0
        t_length = len(ground_truth_sentences)
        for s1, s2, s3 in zip(ground_truth_sentences, nltk_sentences, spacy_sentences):
            cnt += 1
            sentence_ordered_dict = OrderedDict()
            sentence_ordered_dict["index"] = cnt
            sentence_ordered_dict["sentence"] = s1
            sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict))
            sentence_ordered_dict2 = OrderedDict()
            sentence_ordered_dict2["index"] = cnt
            sentence_ordered_dict2["nltk_sentence"] = s2
            sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict2))
            # sentence_ordered_dict3 = OrderedDict()
            # sentence_ordered_dict3["index"] = cnt
            # sentence_ordered_dict3["spacy_sentence"] = s3
            # sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict3))
            # sentence_ordered_dict_list.append(NoIndent({}))

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
    ground_truth_sentences = preprocess.organize_sentences()
    nltk_sentences = preprocess.get_nltk_tokenized_sentences()
    #spacy_sentences = preprocess.get_spacy_tokenized_sentences()
    filtered_sentences = preprocess.get_filtered_sentences(nltk_sentences)
    preprocess.render(ground_truth_sentences, nltk_sentences, spacy_sentences)
