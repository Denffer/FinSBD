import argparse
from dataset import TextDataset
from preprocess import Preprocess
from model.rulebased import RuleBased
from evaluate import Evaluate
from render import Render

class Main:

    def __init__(self, src_path, filename="output.json"):
        self.src = src_path
        self.dst = "output/"
        self.filename = filename

        self.results = []

    def run(self):
    
        # get data
        data = TextDataset(self.src)
        # preprocess
        p = Preprocess(data)
        r = RuleBased()
        e = Evaluate()

        # nltk as baseline
        print("Processsing NLTK as baseline ... ")
        nltk_sentences = r.get_nltk_tokenized_sentences(data.text)
        query_list = p.get_tokenized_words(nltk_sentences)
        
        begin, end, indexed_sentences = e.find_sentence_index(data, query_list)
        breakpoint()

        evaluation = e.evaluate(data, begin, end)
        result = {"key":"nltk", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        self.results.append(result)
        #import pdb; pdb.set_trace()

        # #rule_based methods

        # print("Processsing rule based (Subject) ... ")
        # filtered_sentences = rule_based.filter_subject(nltk_sentences)
        # words = p.get_tokenized_words(filtered_sentences)
        # begin, end, indexed_sentences = p.find_sentence_index(words)
        # evaluation = self.evaluate(data, begin, end)
        # result = {"key":"has_subject", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        # results.append(result)

        # print("Processsing rule based (Verb)... ")
        # words = p.get_tokenized_words(filtered_sentences)
        # begin, end, indexed_sentences = p.find_sentence_index(words)
        # evaluation = self.evaluate(data, begin, end)
        # result = {"key":"has_verb", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        # results.append(result)

        # print("Processsing rule based (Subject & Verb)... ")
        # filtered_sentences = rule_based.filter_verb(filtered_sentences)
        # words = p.get_tokenized_words(filtered_sentences)
        # begin, end, indexed_sentences = p.find_sentence_index(words)
        # evaluation = self.evaluate(data, begin, end)
        # result = {"key":"has_subjectVerb", "begin":begin, "end":end, "sentences":indexed_sentences, "evaluation":evaluation}
        # results.append(result)

        # write result
        print("Writing data to: " + str(self.dst) + "\033[1m" + str(self.filename) + "\033[0m")
        render = Render(self.dst, self.filename, data, p.ground_truth, results)
        render.save()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, required=True, help="path for the source")
    parser.add_argument("--filename", type=str, required=True, help="name for the file")
    args = parser.parse_args()

    main = Main(src_path=args.src,filename=args.filename)
    main.run()
