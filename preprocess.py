from tokenizer import Tokenizer
from tqdm import tqdm
from multiprocessing import Pool

class Preprocess:
    """ preprocess data and get_train """

    def __init__(self, data):
        """ data is the dict from source """
        self.data = data
    
    def get_ground_truth(self):
        """ get ground truth """
        print("Getting ground truth ...")

        # Splitting sentences from raw text in corpus
        ground_truth = []
        for b, e in zip(self.data.begin, self.data.end):
            # add 1 to include the last index
            words = self.data.tokenized_corpus[b:e+1]
            sentence = " ".join(words)

            index = [b,e]
            # grouth_truth = [ [[22, 29], [blah blah ... blah"], * n ]
            ground_truth.append([index, sentence])

        return ground_truth

    def get_nltk_tokenized_sentences(self):
        """ return a list of sentence -> ['sentence1', 'sentence2', ..., 'sentenceN'] """
        #print("Getting nltk result ... ")
        
        tokenizer = Tokenizer()
        tokenized_sentences = tokenizer.text_tokenize(self.data.text)
        return tokenized_sentences
    
    def get_tokenized_words(self, sentences):
        """ return a list of words -> [['word1','word2', ...], ['word1','word2', ...] ...] """
        return [s.split(" ") for s in sentences]

    def find_sentence_index(self, query_list):
        """ return the begin_index & end_index & sentences of the query words """

        sentences, begin, end = [], [], []
        for words in tqdm(query_list):

            sentence, sentence_index = self.get_sublist_index(words, self.data.indexed_corpus)

            if sentence and sentence_index:
                sentences.append([sentence_index, sentence])
                begin.append(sentence_index[0])
                end.append(sentence_index[1])
        #print(begin, end, sentences)
        return begin, end, sentences

    def get_sublist_index(self, sublist, indexed_list):
        """ get the index of sublist in a list """

        sublist_index = []
        sublist_length = len(sublist)
        matched_sentence = ""

        # add filter to filter out sentences if it is too short
        for index in (i for i, e in enumerate(indexed_list) if e[1] == sublist[0] and sublist_length >= 3 ):

            if indexed_list[index+1][1] == sublist[1] and indexed_list[index+2][1] == sublist[2]:
                # turn indexed words into words for comparison
                l = [word[1] for word in indexed_list[index:index+sublist_length]]
                matched_sentence = " ".join(l)
                if l == sublist:
    
                    indexed_l = [word for word in indexed_list[index:index+sublist_length]]
                    begin, end = indexed_l[0][0], indexed_l[-1][0]
                    sublist_index = [begin, end]
                else:
                    continue
            else:
                break

        if matched_sentence and sublist_index:
            return matched_sentence, sublist_index
        else:
            return None, None
            