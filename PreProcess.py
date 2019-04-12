import json, uuid, sys, re, os
import unicodedata
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from collections import OrderedDict
import nltk
from tqdm import tqdm
#import spacy

class PreProcess:
    """ This program aims to preprocess Train_en_new.json in new_dataset """
    """ python version == 3.7 """

    def __init__(self):
        self.src = sys.argv[1]
        self.dst = "new_dataset/"
        self.filename = "clean_train_data.json"

        self.text, self.begin, self.end = [],[],[]
        self.tokenized_corpus = []
        self.verbose = 1

    def get_data(self):
        print("Loading data from: " + "\033[1m" + sys.argv[1] + "\033[0m")

        with open(self.src) as f:
            data = json.load(f)

        self.text = data["text"]
        self.tokenized_corpus = self.text.split(" ")
        self.begin = data["begin_sentence"]
        self.end = data["end_sentence"]

        print("Loading data complete")

    def get_ground_truth(self):
        """ get ground truth """
        print("Getting ground truth ...")

        # Splitting sentences from raw text in corpus
        ground_truth = []
        for b, e in tqdm(zip(self.begin, self.end)):
            filtered_tokenized_corpus = self.tokenized_corpus[b:e]
            sentence = " ".join(filtered_tokenized_corpus)
            #self.clean_text(sentence)

            index = [b,e]
            # grouth_truth = [ [[22, 29], [blah blah ... blah"], * n ]
            ground_truth.append([index, sentence])

        return ground_truth
    
    def get_nltk_result(self):
        """ get nltk result | the format is the same as ground truth """
        print("Getting nltk result ... ")
        
        # tokenizing sentences with NLTK
        nltk_tokenized_sentences = sent_tokenize(self.text)

        # get tokenized_sentence index
        nltk_result = []
        for sentence in tqdm(nltk_tokenized_sentences):
            sentence_index = self.find_sublist_index(sentence, self.tokenized_corpus)

            nltk_result.append([sentence_index, sentence])

        # tokenize every sentence in tokenized_sentences 
        #pos_tagged_sentences = self.get_pos_tagged_sentences(tokenized_sentences)
        #self.filter_sentences(tokenized_sentences)
        #print(sentence_indexes)
        return sentence_indexes

        return tokenized_sentences

    def find_sublist_index(self, sublist, l):
        """ find the index of sublist in a list """

        sublist_index =[]
        sublist_length=len(sublist)
        try:
            for index in (i for i,e in enumerate(l) if e==sublist[0]):
                if l[index:index+sublist_length]==sublist:
                    sublist_index = [index,index+sublist_length-1]
        except:
            sublist_index = [None, None]
   
        # E.g., sublist_index : [22, 49]
        return sublist_index
    
    def get_spacy_tokenized_sentences(self):
        """ bad performance """
        print("Tokenizing sentences with SpaCy ...")

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
        print("Filtering sentences from nltk_sentences ...")
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

        return filtered_sentences


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



    # def evaluate_result(self, text):
    #     """ compare input list with ground truth"""

        

    # def render(self, ground_truth_sentences, nltk_sentences, spacy_sentences):
    def render(self, ground_truth, nltk_result):
        """ put things in order and render json file """

        print("Writing data to: " + str(self.dst) + "\033[1m" + str(self.filename) + "\033[0m")

        ordered_dict = OrderedDict()
        ordered_dict["begin"] = NoIndent(self.begin)
        ordered_dict["end"] = NoIndent(self.end)

        sentence_ordered_dict_list = []
        cnt = 0
        t_length = len(ground_truth_sentences)
        #for s1, s2, s3 in zip(ground_truth_sentences, nltk_sentences, filtered_sentences):
        for s1, s2 in zip(ground_truth, nltk_result):
            cnt += 1
            sentence_ordered_dict = OrderedDict()
            sentence_ordered_dict["cnt"] = cnt
            sentence_ordered_dict["index"] = s1[0]
            # s1 = self.clean_text(s1)
            sentence_ordered_dict["ground_truth"] = s1[1]
            sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict))
            sentence_ordered_dict2 = OrderedDict()
            sentence_ordered_dict2["cnt"] = cnt
            sentence_ordered_dict2["index"] = s2[0]
            sentence_ordered_dict2["nltk_sentence"] = s2[1]
            sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict2))
            sentence_ordered_dict_list.append(NoIndent({}))
            #sentence_ordered_dict3 = OrderedDict()
            #sentence_ordered_dict3["index"] = cnt
            #sentence_ordered_dict3["filtered_sentence"] = s3
            #sentence_ordered_dict_list.append(NoIndent(sentence_ordered_dict3))
            #sentence_ordered_dict_list.append(NoIndent({}))

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
    ground_truth = preprocess.get_ground_truth()
    nltk_result = preprocess.get_nltk_result()
    #spacy_sentences = preprocess.get_spacy_tokenized_sentences()
    #filtered_sentences = preprocess.get_filtered_sentences(nltk_sentences)
    preprocess.render(ground_truth, nltk_result)
