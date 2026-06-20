
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
        self.entry.bind("<Tab>",self.on_tab)

        self.list=tk.Listbox(self.root)
        self.list.pack()

    def update(self,event=None):
        # Extract the last word from input for sentence typing support
        full_text=self.entry.get()
        last_word=full_text.split()[-1] if full_text.split() else ""
        
        words=self.trie.get_suggestions(last_word)
        ranked=Ranker(self.freq).top_k(words)
        self.list.delete(0,tk.END)
        for w in ranked:
            self.list.insert(tk.END,w)
    
    def on_tab(self,event=None):
        # Prevent TAB from inserting suggestion automatically
        # TAB should only accept when explicitly intended (e.g., via button click)
        return "break"  # Consume the TAB event, don't insert default behavior

    def run(self):
        self.root.mainloop()
