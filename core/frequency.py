
import json, os

class FrequencyEngine:
    """
    Manages word frequency for Romanized Nepali autocomplete system.
    Provides safe file I/O with atomic writes to prevent data loss.
    """
    def __init__(self, path):
        self.path = path
        self.frequency = {}
        self.load()

    def load(self):
        """Load frequency dictionary from JSON file."""
        if os.path.exists(self.path):
            try:
                with open(self.path, encoding="utf-8") as f:
                    self.frequency = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading frequency file: {e}. Starting fresh.")
                self.frequency = {}

    def save(self):
        """Save frequency dictionary to JSON file atomically."""
        try:
            # Write to temporary file first
            temp_path = self.path + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.frequency, f, indent=4, ensure_ascii=False)
            # Atomic rename (move temp to target)
            os.replace(temp_path, self.path)
        except IOError as e:
            print(f"Error saving frequency file: {e}")

    def update(self, word):
        """
        Update frequency for a word and persist to disk.
        If word doesn't exist, initialize with frequency = 1.
        """
        word = word.strip().lower()
        if not word:
            return
        self.frequency[word] = self.frequency.get(word, 0) + 1
        self.save()

    def get(self, word):
        """Get frequency of a word (default 0 if not found)."""
        return self.frequency.get(word.lower(), 0)

    def get_all(self):
        """Return entire frequency dictionary."""
        return self.frequency
