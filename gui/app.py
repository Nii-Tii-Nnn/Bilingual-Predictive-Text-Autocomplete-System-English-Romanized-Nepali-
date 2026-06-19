
import tkinter as tk
from core.trie import Trie
from core.dataset import DatasetManager
from core.frequency import FrequencyEngine
from core.ranker import Ranker

class PredictiveTextGUI:
    def __init__(self):
        self.trie=Trie()
        self.freq=FrequencyEngine("data/frequency.json")
        for w in DatasetManager("data/dictionary.txt").load():
            self.trie.insert(w)
        self.root=tk.Tk()
        self.root.title("Bilingual Predictive Text")

        self.entry=tk.Entry(self.root,width=50)
        self.entry.pack()
        self.entry.bind("<KeyRelease>",self.update)

        self.list=tk.Listbox(self.root)
        self.list.pack()

    def update(self,event=None):
        words=self.trie.get_suggestions(self.entry.get())
        ranked=Ranker(self.freq).top_k(words)
        self.list.delete(0,tk.END)
        for w in ranked:
            self.list.insert(tk.END,w)

    def run(self):
        self.root.mainloop()
