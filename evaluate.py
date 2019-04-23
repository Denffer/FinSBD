import json, argparse
from dataset import TextDataset
from preprocess import Preprocess
from tokenizer import Tokenizer
from model.rule_based import RuleBased
from render import Render
#import spacy

class Evaluate:
    """ python version : 3.6 """

    def __init__(self, src_path, filename="output.json"):
        self.src = src_path
        self.dst = "output/"
        self.filename = filename

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

    def run(self):
        # get data
        data = TextDataset(self.src)
        # preprocess
        p = Preprocess(data)
        ground_truth = p.get_ground_truth()
        results = []

        # nltk as baseline
        print("Processsing NLTK as baseline ... ")
        nltk_sentences = p.get_nltk_tokenized_sentences()
        query_list = p.get_tokenized_words(nltk_sentences)
        
        begin, end, indexed_sentences = p.find_sentence_index(query_list)
        evaluation = self.evaluate(data, begin, end)
        result = {"key":"nltk", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        results.append(result)

        #rule_based methods
        rule_based = RuleBased()

        print("Processsing rule based (Subject) ... ")
        filtered_sentences = rule_based.filter_subject(nltk_sentences)
        words = p.get_tokenized_words(filtered_sentences)
        begin, end, indexed_sentences = p.find_sentence_index(words)
        evaluation = self.evaluate(data, begin, end)
        result = {"key":"has_subject", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        results.append(result)

        print("Processsing rule based (Verb)... ")
        words = p.get_tokenized_words(filtered_sentences)
        begin, end, indexed_sentences = p.find_sentence_index(words)
        evaluation = self.evaluate(data, begin, end)
        result = {"key":"has_verb", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        results.append(result)

        print("Processsing rule based (Subject & Verb)... ")
        filtered_sentences = rule_based.filter_verb(filtered_sentences)
        words = p.get_tokenized_words(filtered_sentences)
        begin, end, indexed_sentences = p.find_sentence_index(words)
        evaluation = self.evaluate(data, begin, end)
        result = {"key":"has_subjectVerb", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        results.append(result)

        # write result
        print("Writing data to: " + str(self.dst) + "\033[1m" + str(self.filename) + "\033[0m")
        render = Render(self.dst, self.filename, data, ground_truth, results)
        render.save()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, required=True, help="path for the source")
    parser.add_argument("--filename", type=str, required=True, help="name for the file")
    args = parser.parse_args()

    main = Evaluate(src_path=args.src,filename=args.filename)
    main.run()
