
import tkinter as tk
from core.trie import Trie
from core.dataset import DatasetManager
from core.frequency import FrequencyEngine
from core.ranker import Ranker

class PredictiveTextGUI:
    """
    Romanized Nepali Autocomplete GUI.
    Supports sentence typing with per-word suggestions.
    Dynamically updates word frequency based on user selection.
    """
    def __init__(self):
        self.trie = Trie()
        self.freq = FrequencyEngine("data/frequency.json")
        self.dict_path = "data/dictionary.txt"
        
        # Load dictionary and populate trie
        for w in DatasetManager(self.dict_path).load():
            self.trie.insert(w)
        self.loaded_words = set(DatasetManager(self.dict_path).load())
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title("Romanized Nepali Autocomplete")
        self.root.geometry("600x400")
        
        # Input field
        tk.Label(self.root, text="Type Nepali (romanized):", font=("Arial", 10)).pack(pady=5)
        self.entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<KeyRelease>", self.update_suggestions)
        self.entry.bind("<Tab>", self.on_tab)
        self.entry.bind("<Return>", self.on_enter)
        
        # Suggestions listbox
        tk.Label(self.root, text="Suggestions:", font=("Arial", 10)).pack(pady=5)
        self.list = tk.Listbox(self.root, height=10, font=("Arial", 11))
        self.list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.list.bind("<Double-Button-1>", self.on_suggestion_selected)
        
        # Status bar
        self.status = tk.Label(self.root, text="Ready", fg="green", font=("Arial", 9))
        self.status.pack(pady=5)
        
        # Current word being typed (for tracking)
        self.current_word = ""

    def normalize_input(self, text):
        """Normalize input: lowercase and strip whitespace."""
        return text.strip().lower()

    def extract_last_word(self, text):
        """
        Extract last word from input for sentence handling.
        Example: "how are" -> "are"
        """
        words = text.split()
        if not words:
            return ""
        return words[-1]

    def get_prefix_context(self):
        """Get full text and the prefix (last word) for suggestions."""
        full_text = self.entry.get()
        prefix = self.extract_last_word(full_text)
        return full_text, self.normalize_input(prefix)

    def update_suggestions(self, event=None):
        """Update suggestion list based on current input."""
        if event and event.keysym == "Tab":
            return  # Skip update for Tab key
        
        full_text, prefix = self.get_prefix_context()
        
        # Get suggestions from trie
        if prefix:
            words = self.trie.get_suggestions(prefix)
            ranked = Ranker(self.freq).top_k(words)
        else:
            ranked = []
        
        # Update listbox
        self.list.delete(0, tk.END)
        for i, w in enumerate(ranked):
            freq_score = self.freq.get(w)
            display = f"{w} ({freq_score})"
            self.list.insert(tk.END, display)

    def on_suggestion_selected(self, event=None):
        """Handle double-click on suggestion to insert it."""
        selection = self.list.curselection()
        if not selection:
            return
        
        selected_item = self.list.get(selection[0])
        word = selected_item.split(" (")[0] if " (" in selected_item else selected_item
        self.accept_suggestion(word)

    def get_active_suggestion(self):
        """Return the highlighted suggestion or the first visible suggestion."""
        selection = self.list.curselection()
        if selection:
            item = self.list.get(selection[0])
            return item.split(" (")[0] if " (" in item else item

        if self.list.size() > 0:
            item = self.list.get(0)
            return item.split(" (")[0] if " (" in item else item

        return None

    def accept_suggestion(self, word):
        """Accept and insert a suggestion, update frequency and dictionary."""
        full_text = self.entry.get()
        words = full_text.split()
        
        # Replace last word with suggestion
        if words:
            words[-1] = word
        else:
            words = [word]
        
        new_text = " ".join(words)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, new_text + " ")
        self.entry.focus()
        
        # Update frequency
        self.freq.update(word)
        
        # Add to dictionary if new word
        if word not in self.loaded_words:
            self.add_word_to_dictionary(word)
        
        self.status.config(text=f"✓ Selected: {word}", fg="green")
        self.update_suggestions()

    def add_word_to_dictionary(self, word):
        """Add a new word to dictionary.txt if not already present."""
        word = word.strip().lower()
        if not word or word in self.loaded_words:
            return
        
        try:
            # Append to dictionary file
            with open(self.dict_path, "a", encoding="utf-8") as f:
                f.write(word + "\n")
            # Update in-memory set and trie
            self.loaded_words.add(word)
            self.trie.insert(word)
        except IOError as e:
            print(f"Error adding word to dictionary: {e}")

    def on_tab(self, event=None):
        """Accept the highlighted suggestion with TAB key."""
        word = self.get_active_suggestion()
        if word:
            self.accept_suggestion(word)
        return "break"

    def on_enter(self, event=None):
        """Accept the highlighted suggestion with Enter key, or confirm typed word."""
        full_text = self.entry.get().strip()
        if not full_text:
            return "break"
        
        # If a suggestion is highlighted, accept it
        word = self.get_active_suggestion()
        if word:
            self.accept_suggestion(word)
        else:
            # No highlight, confirm the last word as typed
            last_word = self.extract_last_word(full_text)
            if last_word:
                self.freq.update(last_word)
                if last_word not in self.loaded_words:
                    self.add_word_to_dictionary(last_word)
                self.status.config(text=f"✓ Confirmed: {last_word}", fg="green")
        
        self.entry.delete(0, tk.END)
        self.update_suggestions()
        return "break"

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
