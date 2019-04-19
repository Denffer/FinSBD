from collections import OrderedDict
import json
#import pdb; pdb.set_trace()

class Render:
    """ Put things in order and save json file """
    def __init__(self, dst_path, data, ground_truth, *results):
        self.dst_path = dst_path
        self.data = data
        self.ground_truth = ground_truth
        self.results = list(results)

        self.output = OrderedDict()
        self.write_default()
        for i, result in enumerate(self.results):
            self.write_evaluation(result)
            if i == len(self.results)-1:
                self.write_sentences(self.results[-1])
            else:
                continue

    def write_default(self):
        self.output["begin"] = NoIndent(self.data.begin)
        self.output["end"] = NoIndent(self.data.end)
    
    def write_evaluation(self, result):
        key = result["key"]
        self.output[key+"_begin"] = NoIndent(result["begin"])
        self.output[key+"_end"] = NoIndent(result["end"])
        self.output[key+"_evaluation"] = NoIndent(result["evaluation"])

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
        f = open(self.dst_path + "/output.json", 'w+')
        f.write(json.dumps(self.output, indent = 4, default=default))

class NoIndent(object):
    def __init__(self, value):
        self.value = value

def default(o, encoder=json.JSONEncoder()):
    if isinstance(o, NoIndent):
        return json.dumps(o.value)
    return encoder.default(o)