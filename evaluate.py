import json, sys
import argparse
import unicodedata
from tokenizer import Tokenizer
from collections import OrderedDict
from dataset import TextDataset
import nltk
from tqdm import tqdm
import spacy

class Evaluate:
    """ python version : 3.7 """

    def __init__(self, src, dst="output/"):
        self.src = src
        #self.dst = "output/"
        self.dst = dst

        # self.text, self.begin, self.end = [],[],[]
        # self.tokenized_corpus = []
        # self.verbose = 1

    def get_ground_truth(self, data):
        """ get ground truth """
        print("Getting ground truth ...")

        # Splitting sentences from raw text in corpus
        ground_truth = []
        for b, e in zip(data.begin, data.end):
            # add 1 to include the last index
            words = data.tokenized_corpus[b:e+1]
            sentence = " ".join(words)

            index = [b,e]
            # grouth_truth = [ [[22, 29], [blah blah ... blah"], * n ]
            ground_truth.append([index, sentence])

        return ground_truth
    
    def get_nltk_result(self, data):
        print("Getting nltk result ... ")
        
        tokenizer = Tokenizer()
        tokenized_sentences = tokenizer.text_tokenize(data.text)
        tokenized_words = [s.split(" ") for s in tokenized_sentences]

        # get tokenized_sentence index
        result, sentences, begin, end = [], [], [], []
        for words in tqdm(tokenized_words):

            sentence_index, tarket_words = self.find_sublist_index(words, data.tokenized_corpus)
            sentence = " ".join(tarket_words)

            # filter out sentences if it is too short
            if int(sentence_index[1]) - int(sentence_index[0]) >= 5:
                #sentence = self.clean_text(sentence)
                sentences.append([sentence_index, sentence])
                begin.append(sentence_index[0])
                end.append(sentence_index[1])
            else:
                pass

        evaluation = self.evaluate(data, begin, end)
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

    def evaluate(self, data, begin, end):
        """ check the percentage hit rate as compared to ground truth """
        
        begin_hit = 0
        for e in begin:
            if e in data.begin:
                begin_hit += 1
        begin_hit_rate = float(begin_hit / len(begin))

        end_hit = 0
        for e in end:
            if e in data.end:
                end_hit += 1
        end_hit_rate = float(end_hit / len(end))

        evaluation = [begin_hit_rate, end_hit_rate]

        return evaluation

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

    def render(self, data, ground_truth, nltk_result):
        """ put things in order and render json file """

        print("Writing data to: " + str(self.dst) + "\033[1m" + "nltk_output.txt" + "\033[0m")

        result = OrderedDict()
        result["begin"] = NoIndent(data.begin)
        result["end"] = NoIndent(data.end)
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

            # if self.verbose:
            #     sys.stdout.write("\rStatus: %s / %s"%(cnt, g_length))
            #     sys.stdout.flush()
                
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
            
            # if self.verbose:
            #     sys.stdout.write("\rStatus: %s / %s"%(cnt, n_length))
            #     sys.stdout.flush()

        result["nltk_result"] = nltk_sentence_list

        f = open(self.dst + "/nltk_result.json", 'w+')
        f.write(json.dumps(result, indent = 4, default=default))
    
    def run(self):

        data = TextDataset(self.src)


        #self.get_data()
        #preprocess.dump_small_dataset()
        ground_truth = self.get_ground_truth(data)
        nltk_result = self.get_nltk_result(data)
        #spacy_sentences = preprocess.get_spacy_tokenized_sentences()
        #filtered_sentences = preprocess.get_filtered_sentences(nltk_sentences)
        self.render(data, ground_truth, nltk_result)


class NoIndent(object):
    def __init__(self, value):
        self.value = value

def default(o, encoder=json.JSONEncoder()):
    if isinstance(o, NoIndent):
        return json.dumps(o.value)
    return encoder.default(o)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, required=True, help="path for the source")
    
    args = parser.parse_args()

    main = Evaluate(src=args.src)
    main.run()
