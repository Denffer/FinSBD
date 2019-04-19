import json, argparse
from dataset import TextDataset
from preprocess import Preprocess
from tokenizer import Tokenizer
from render import Render
#import spacy

class Evaluate:
    """ python version : 3.6 """

    def __init__(self, src_path, dst_path="output/"):
        self.src = src_path
        self.dst = dst_path

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
    
    def run(self):
        
        # get data
        data = TextDataset(self.src)

        # preprocess
        preprocessor = Preprocess(data)
        ground_truth = preprocessor.get_ground_truth(data)
        nltk_sentences = preprocessor.get_nltk_tokenized_sentences(data)
        nltk_words = preprocessor.get_tokenized_words(nltk_sentences)
        
        # nltk as baseline
        nltk_begin, nltk_end, nltk_sentences = preprocessor.find_sentence_index(data, nltk_words)
        nltk_evaluation = self.evaluate(data, nltk_begin, nltk_end)
        nltk_result = {"key":"nltk", "begin":nltk_begin, "end":nltk_end, "sentences":nltk_sentences, "evaluation":nltk_evaluation}

        # start making changes

        # write result
        print("Writing data to: " + str(self.dst) + "\033[1m" + "output.txt" + "\033[0m")
        render = Render(self.dst, data, ground_truth, nltk_result)
        render.save()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, required=True, help="path for the source")
    args = parser.parse_args()

    main = Evaluate(src_path=args.src)
    main.run()
