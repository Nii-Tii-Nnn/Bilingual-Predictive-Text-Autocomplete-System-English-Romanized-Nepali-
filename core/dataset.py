
class DatasetManager:
    def __init__(self,file):
        self.file=file

    def load(self):
        with open(self.file,encoding="utf-8") as f:
            return list(set(
                x.strip().replace(" ","_")
                for x in f if x.strip()
            ))
