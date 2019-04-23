from collections import OrderedDict
import json

class Render:
    """ Put things in order and save json file """
    def __init__(self, dst_path, filename, data, ground_truth, results):
        self.dst_path = dst_path
        self.filename = filename
        self.data = data
        # self.ground_truth = ground_truth # ground truth is the sentences
        self.results = results

        self.output = OrderedDict()
        self.run()

    def run(self):

        separator = "-"
        self.write_default(separator)
        for i, result in enumerate(self.results):
            if i == len(self.results)-1:
                #print(i, len(self.results))
                self.write_evaluation(result, separator*(i+2))
                self.write_sentences(result)
            else:
                #print(i, len(self.results))
                self.write_evaluation(result, separator*(i+2)) 

    def write_default(self, separator):

        self.output["ground_truth_begin"] = NoIndent(self.data.begin)
        self.output["ground_truth_end"] = NoIndent(self.data.end)
        self.output["ground_truth_total_cnt"] = NoIndent(len(self.data.begin))
        self.output[separator] = {}

    
    def write_evaluation(self, result, separator):
        key = result["key"]
        self.output[key+"_begin"] = NoIndent(result["begin"])
        self.output[key+"_end"] = NoIndent(result["end"])
        self.output[key+"_total_cnt"] = NoIndent(len(result["begin"]))
        self.output[key+"_evaluation"] = NoIndent(result["evaluation"])
        self.output[separator] = {}

    def write_sentences(self, result):

        sentences = result["sentences"]
        key = result["key"]

        sentence_list = []
        cnt = 0
        for s in sentences:
            cnt += 1
            sentence = OrderedDict()
            sentence["cnt"] = cnt
            sentence["index"] = s[0]
            sentence["sentence"] = s[1]
            sentence_list.append(NoIndent(sentence))
            
        key += "_result"
        self.output[key] = sentence_list

    def save(self):
        f = open(self.dst_path + self.filename, 'w+')
        f.write(json.dumps(self.output, indent = 4, default=default))

class NoIndent(object):
    def __init__(self, value):
        self.value = value

def default(o, encoder=json.JSONEncoder()):
    if isinstance(o, NoIndent):
        return json.dumps(o.value)
    return encoder.default(o)