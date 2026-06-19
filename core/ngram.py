
class NGram:
    def __init__(self):
        self.data={}

    def train(self,text):
        words=text.split()
        for a,b in zip(words,words[1:]):
            self.data.setdefault(a,{})
            self.data[a][b]=self.data[a].get(b,0)+1

    def predict(self,word):
        if word not in self.data:
            return []
        return sorted(
            self.data[word],
            key=self.data[word].get,
            reverse=True
        )
