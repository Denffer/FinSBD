import json, argparse
from tqdm import tqdm

class Evaluate:
    """ python version : 3.6 """

    def __init__(self):
        pass

    def find_sentence_index(self, data, query_list):
        """ return the begin_index & end_index & sentences of the query words """

        idx_tokens = data.clean_idx_tokens

        sentences, begin, end = [], [], []
        # boundry is set as the beginning infex of the indexed_corpus -> speed up the process
        boundary = 0
        for words in tqdm(query_list):
            
            sentence, sentence_index = self.get_sublist_index(idx_tokens[boundary:], words)

            if sentence and sentence_index:
                sentences.append([sentence_index, sentence])
                begin.append(sentence_index[0])
                end.append(sentence_index[1])

                boundary = sentence_index[1]
        #print(begin, end, sentences)
        return begin, end, sentences

    def get_sublist_index(self, indexed_list, sublist):
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
            #print(sublist)
            return None, None

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
