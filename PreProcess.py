import json, uuid, sys, re, os
import unicodedata
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from collections import OrderedDict
import nltk
from tqdm import tqdm
import spacy

class PreProcess:
    """ This program aims to preprocess Train_en_new.json in new_dataset """
    """ python version == 3.7 """

    def __init__(self):
        self.src = sys.argv[1]
        self.dst = "new_dataset/"
        self.filename = "output.json"

        self.text, self.begin, self.end = [],[],[]
        self.tokenized_corpus = []
        self.verbose = 1

    def get_data(self):
        print("Loading data from: " + "\033[1m" + sys.argv[1] + "\033[0m")

        with open(self.src) as f:
            data = json.load(f)

        self.text = data["text"].replace("\n","")
        self.tokenized_corpus = self.text.split(" ")
        self.begin = data["begin_sentence"]
        self.end = data["end_sentence"]

        print("Loading data complete")

    def get_ground_truth(self):
        """ get ground truth """
        print("Getting ground truth ...")

        # cnt = 0
        # for w in self.tokenized_corpus:
        #     print(cnt, w)
        #     cnt += 1
        # Splitting sentences from raw text in corpus
        ground_truth = []
        for b, e in zip(self.begin, self.end):
            # add 1 to include the last index
            words = self.tokenized_corpus[b:e+1]
            sentence = " ".join(words)

            index = [b,e]
            # grouth_truth = [ [[22, 29], [blah blah ... blah"], * n ]
            ground_truth.append([index, sentence])

        return ground_truth
    
    def get_nltk_result(self):
        """ get nltk result | the format is the same as ground truth """
        print("Getting nltk result ... ")
        
        # tokenizing sentences with NLTK
        tokenized_sentences = sent_tokenize(self.text)
        tokenized_words = [s.split(" ") for s in tokenized_sentences]

        # get tokenized_sentence index
        result, sentences, begin, end = [], [], [], []
        for words in tqdm(tokenized_words):

            sentence_index, tarket_words = self.find_sublist_index(words, self.tokenized_corpus)
            sentence = " ".join(tarket_words)

            # filter out sentences if it is too short
            if int(sentence_index[1]) - int(sentence_index[0]) >= 5:
                #sentence = self.clean_text(sentence)
                sentences.append([sentence_index, sentence])
                begin.append(sentence_index[0])
                end.append(sentence_index[1])
            else:
                pass

        evaluation = self.evaluate(begin, end)
        result = {"begin":begin, "end":end, "sentences":sentences, "evaluation":evaluation}

        return result

    def find_sublist_index(self, sublist, l):
        """ find the index of sublist in a list """

        sublist_index = []
        sublist_length = len(sublist)
        for index in (i for i,e in enumerate(l) if e == sublist[0]):
            if l[index:index+sublist_length] == sublist:
                sublist_index = [index,index+sublist_length-1]
            else:
                continue
                
        # E.g., sublist : ["word1", "word2", ...] sublist_index : [22, 49]
        return sublist_index, sublist

    def evaluate(self, begin, end):
        """ check the percentage hit rate as compared to ground truth """
        
        begin_hit = 0
        for e in begin:
            if e in self.begin:
                begin_hit += 1
        begin_hit_rate = float(begin_hit / len(begin))

        end_hit = 0
        for e in end:
            if e in self.end:
                end_hit += 1
        end_hit_rate = float(end_hit / len(end))

        evaluation = [begin_hit_rate, end_hit_rate]

        return evaluation

    def clean_text(self, text):
        """ customized clean text """
        # remove unnecessary digits
        text =re.sub(r'\s\d\s\.', '', text)
        # remove all punctuation
        #text = re.sub("([^\w\s]|\_)",r' ', text)
        text = text.encode().decode('utf-8')
        # remove extra spaces
        clean_text = re.sub(r'(\s)+', r' ', text)

        return clean_text
    

    
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

    def render(self, ground_truth, nltk_result):
        """ put things in order and render json file """

        print("Writing data to: " + str(self.dst) + "\033[1m" + str(self.filename) + "\033[0m")

        result = OrderedDict()
        result["begin"] = NoIndent(self.begin)
        result["end"] = NoIndent(self.end)
        result["nltk_begin"] = NoIndent(nltk_result["begin"])
        result["nltk_end"] = NoIndent(nltk_result["end"])
        result["nltk_evaluation"] = NoIndent(nltk_result["evaluation"])

        sentence_list = []
        cnt = 0
        g_length = len(ground_truth)
        #for s1, s2, s3 in zip(ground_truth_sentences, nltk_sentences, filtered_sentences):
        for s in ground_truth:
            cnt += 1
            sentence = OrderedDict()
            sentence["cnt"] = cnt
            sentence["index"] = s[0]
            sentence["sentence"] = s[1]
            sentence_list.append(NoIndent(sentence))

            if self.verbose:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, g_length))
                sys.stdout.flush()
                
        result["ground_truth"] = sentence_list

        nltk_sentence_list = []
        cnt = 0
        n_length = len(nltk_result)
        for s in nltk_result["sentences"]:
            cnt += 1
            sentence = OrderedDict()
            sentence["cnt"] = cnt
            sentence["index"] = s[0]
            sentence["sentence"] = s[1]
            nltk_sentence_list.append(NoIndent(sentence))
            
            if self.verbose:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, n_length))
                sys.stdout.flush()

        result["nltk_result"] = nltk_sentence_list

        f = open(self.dst + "/" + self.filename, 'w+')
        f.write(json.dumps(result, indent = 4, default=default))

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
    #preprocess.dump_small_dataset()
    ground_truth = preprocess.get_ground_truth()
    nltk_result = preprocess.get_nltk_result()
    #spacy_sentences = preprocess.get_spacy_tokenized_sentences()
    #filtered_sentences = preprocess.get_filtered_sentences(nltk_sentences)
    preprocess.render(ground_truth, nltk_result)
