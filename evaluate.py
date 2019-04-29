import json, argparse
from tqdm import tqdm

class Evaluate:
    """ python version : 3.6 """

    def __init__(self):
        pass

    def find_query_index(self, idx_tokens, query_list):
        """ return the begin_index & end_index & sentences of the query words """

        sentences, begin, end = [], [], []
        # boundry is set as the beginning infex of the indexed_corpus -> speed up the process
        #print("ori:",idx_tokens)
        for words in tqdm(query_list):
            
            sentence, sentence_index = self.get_sublist_index(idx_tokens, words)


            if sentence and sentence_index:
                sentences.append([sentence_index, sentence])
                begin.append(sentence_index[0])
                end.append(sentence_index[1])

                for i, tok in enumerate(idx_tokens):
                    if tok[0] == sentence_index[1]:
                        idx_tokens = idx_tokens[i+1:]
                        #print("trimmed:",idx_tokens)
                        break


        return begin, end, sentences

    def get_sublist_index(self, idx_tokens, sublist):
        """ get the index of sublist in a list """

        sublist_index = []
        sublist_length = len(sublist)
        matched_sentence = ""
        
        for index in (i for i, e in enumerate(idx_tokens) if e[1] == sublist[0] and len(sublist) > 1 ):
            
            if idx_tokens[index][1] == sublist[0]:
                #print("hit:", sublist)

                # turn indexed words into words for comparison
                l = [word[1] for word in idx_tokens[index:index+sublist_length]]
                matched_sentence = " ".join(l)
                if l == sublist:
        
                    indexed_l = [word for word in idx_tokens[index:index+sublist_length]]
                    begin, end = indexed_l[0][0], indexed_l[-1][0]
                    sublist_index = [begin, end]

                else:
                    continue
            else:
                break

        if matched_sentence and sublist_index:
            #print(matched_sentence)
            return matched_sentence, sublist_index
        else:
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
