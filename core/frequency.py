
import json, os

class FrequencyEngine:
    def __init__(self,path):
        self.path=path
        self.frequency={}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path,encoding="utf-8") as f:
                self.frequency=json.load(f)

    def save(self):
        with open(self.path,"w",encoding="utf-8") as f:
            json.dump(self.frequency,f,indent=4)

    def update(self,word):
        self.frequency[word]=self.frequency.get(word,0)+1

    def get(self,word):
        return self.frequency.get(word,0)
