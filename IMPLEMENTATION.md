# Romanized Nepali Autocomplete System - Implementation Guide

## Overview
This is a complete autocomplete system for Romanized Nepali text input. Users type Nepali words using English letters (e.g., "namaste", "k cha", "ma janchu") and receive intelligent suggestions ranked by frequency.

## Features Implemented

### 1. Dictionary Management
- **File**: `data/dictionary.txt`
- **Module**: `core/dataset.py`
- Loads all valid romanized Nepali words
- Handles duplicates automatically (converts to set)
- Normalizes underscores in compound words (e.g., "k_cha")

**Usage**:
```python
from core.dataset import DatasetManager
dm = DatasetManager("data/dictionary.txt")
words = dm.load()  # Returns list of unique words
```

### 2. Trie Data Structure (Prefix Tree)
- **File**: `core/trie.py`
- O(1) insertions and O(m) prefix searches (m = prefix length)
- Efficient for autocomplete scenarios

**Methods**:
- `insert(word)` - Add word to trie
- `search(word)` - Check if complete word exists
- `starts_with(prefix)` - Check if prefix exists
- `get_suggestions(prefix)` - Get all words matching prefix

### 3. Frequency Engine (Dynamic Learning)
- **File**: `core/frequency.py`
- **Key Features**:
  - Loads frequency data from `data/frequency.json`
  - Tracks word usage frequency
  - **Atomic writes**: Uses temporary file + rename to prevent data loss
  - **Error handling**: Recovers gracefully on corrupted JSON
  - **Auto-persistence**: `save()` called automatically after each update
  - **Normalization**: All words stored in lowercase

**Key Methods**:
```python
freq = FrequencyEngine("data/frequency.json")

# Update frequency and persist immediately
freq.update("namaste")  # Increases frequency and saves to disk

# Retrieve word frequency
count = freq.get("namaste")  # Returns 0 if word not found

# Get full dictionary
all_freqs = freq.get_all()  # Returns {word: frequency} dict
```

**File Safety**:
- Writes to temporary file first
- Atomically renames temp to target (prevents incomplete writes)
- Handles IOError exceptions gracefully

### 4. Ranking Engine (Top-K)
- **File**: `core/ranker.py`
- **Algorithm**: Heap-based Top-K ranking
- **Complexity**: O(n log k) for ranking
- **Behavior**: Higher frequency = higher priority

**Usage**:
```python
from core.ranker import Ranker
ranker = Ranker(freq_engine)
top_5 = ranker.top_k(["hello", "hi", "help"], k=5)
```

### 5. GUI with Dynamic Frequency Updates
- **File**: `gui/app.py`
- **Interactive Features**:
  - Real-time suggestions as user types
  - Frequency scores displayed with suggestions
  - Double-click to select suggestion
  - Enter key to confirm word
  - Status bar for user feedback

**Key GUI Features**:

#### Sentence Handling
- Input: "how are you"
- Extracts last word: "you"
- Provides suggestions only for "you", not the entire input
- Only the last confirmed word updates frequency

#### Tab Key Prevention
- TAB key no longer auto-inserts suggestions
- Users must explicitly double-click or use Enter
- Prevents accidental insertions

#### Frequency Display
- Shows: `word (frequency_count)`
- Example: `namaste (120)`
- Helps users understand word popularity

#### Input Normalization
- All input converted to lowercase
- Handles mixed-case input gracefully
- "NAMASTE", "Namaste", "namaste" all treated identically

### 6. Complete Workflow

#### Example 1: User Types "k"
```
1. User types "k"
2. System extracts last word: "k"
3. Trie returns all words starting with "k": ["k_cha", "ke_gardai"]
4. Ranker sorts by frequency
5. GUI displays:
   - k_cha (90)
   - ke_gardai (0)
6. User double-clicks "k_cha"
7. frequency.json updated: "k_cha" frequency increases by 1
8. Text in input: "k_cha "
```

#### Example 2: User Types "how are"
```
1. User types "how " → gets suggestions for "how"
2. Selects or confirms
3. User types "are" → gets suggestions for "are" ONLY
4. The "how" part stays fixed, only "are" gets suggestions
5. Selecting "are" updates its frequency, not "how"
```

## Implementation Details

### Atomic File Operations
```python
# Core safety pattern used in frequency.py
def save(self):
    temp_path = self.path + ".tmp"
    # Write to temp file
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(self.frequency, f, indent=4)
    # Atomic rename (prevents partial writes)
    os.replace(temp_path, self.path)
```

### Input Normalization
```python
def normalize_input(text):
    return text.strip().lower()
```

### Sentence Parsing
```python
def extract_last_word(text):
    words = text.split()
    return words[-1] if words else ""
    # "how are you" → "you"
    # "hello " → ""
```

## Data Files

### `data/dictionary.txt`
```
hello
hi
computer
engineering
project
namaste
k_cha
```

### `data/frequency.json`
```json
{
    "hello": 120,
    "computer": 45,
    "engineering": 30,
    "sanchai": 75,
    "ramro": 60,
    "huncha": 40
}
```

This file is **automatically updated** when users select words.

## Testing

Run the comprehensive test suite:
```bash
python test_romanized_nepali.py
```

Tests cover:
1. Dictionary loading
2. Trie operations
3. Frequency persistence
4. Ranking algorithm
5. Sentence handling
6. Input normalization
7. Full workflow

## Usage

### Start the GUI
```bash
python main.py
```

### Programmatic Usage
```python
from core.trie import Trie
from core.dataset import DatasetManager
from core.frequency import FrequencyEngine
from core.ranker import Ranker

# Setup
dm = DatasetManager("data/dictionary.txt")
trie = Trie()
for word in dm.load():
    trie.insert(word)

freq = FrequencyEngine("data/frequency.json")
ranker = Ranker(freq)

# Get suggestions
prefix = "nam"
suggestions = trie.get_suggestions(prefix)  # ["namaste"]
ranked = ranker.top_k(suggestions, k=5)     # Sort by frequency

# Update frequency (automatic in GUI)
freq.update("namaste")  # Frequency increases by 1, persists to disk
```

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Dictionary load | O(n) | Linear in number of words |
| Trie insert | O(m) | m = word length |
| Trie search | O(m) | m = word length |
| Prefix matching | O(m + k) | m = prefix length, k = results |
| Ranking | O(n log k) | n = suggestions, k = top results |
| Frequency update | O(1) + I/O | Constant time + file write |

## Error Handling

### Corrupted frequency.json
```
System detects JSONDecodeError
Prints: "Error loading frequency file: ..."
Starts with fresh empty dictionary
No data loss
```

### Missing dictionary.txt
```
System raises FileNotFoundError
User must ensure dictionary exists
```

### Disk write failure
```
System prints: "Error saving frequency file: ..."
In-memory frequency updated
But not persisted (user awareness needed)
```

## Bonus Features Implemented

✓ Lowercase normalization  
✓ Duplicate word handling  
✓ Atomic file writes (crash-safe)  
✓ Error recovery  
✓ Input validation  
✓ Frequency display in GUI  
✓ Status bar feedback  
✓ Sentence support  
✓ Per-word frequency updates  

## Future Enhancements

- [ ] Fuzzy matching with Levenshtein distance (already in codebase)
- [ ] N-gram based next-word prediction (already in codebase)
- [ ] Multi-language support
- [ ] User profiles with separate frequency tracking
- [ ] Export/import frequency data
- [ ] Analytics dashboard

## Requirements

- Python 3.10+
- tkinter (included with Python)
- No external packages required

## Author Notes

This implementation prioritizes:
1. **Data Safety**: Atomic writes prevent corruption
2. **Modularity**: Each component has clear responsibility
3. **Performance**: Trie + heap-based ranking for speed
4. **User Experience**: Sentence typing, frequency display, clear feedback
5. **Robustness**: Error handling and recovery mechanisms
