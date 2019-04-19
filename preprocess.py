from tokenizer import Tokenizer
from tqdm import tqdm

class Preprocess:
    """ preprocess data and get_train """

    def __init__(self, data):
        """ data is the dict from source """
        self.data = data
    
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

    def get_nltk_tokenized_sentences(self, data):
        """ return a list of sentence -> ['sentence1', 'sentence2'...] """
        #print("Getting nltk result ... ")
        
        tokenizer = Tokenizer()
        tokenized_sentences = tokenizer.text_tokenize(data.text)
        return tokenized_sentences
    
    def get_tokenized_words(self, sentences):
        """ return a list of words -> [['word1','word2', ...], ['word1','word2', ...] ...] """
        return [s.split(" ") for s in sentences]
        

    def find_sentence_index(self, data, tokenized_words):
        """ return the begin_index & end_index & sentences of the query words """

        sentences, begin, end = [], [], []
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
                continue

        return begin, end, sentences
    
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
    