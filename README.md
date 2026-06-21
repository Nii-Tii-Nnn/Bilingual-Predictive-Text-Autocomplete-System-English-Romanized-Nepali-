
# Bilingual Predictive Text & Autocomplete System
## Romanized Nepali Autocomplete

Semester-level Python Computer Engineering project implementing a complete autocomplete system for romanized Nepali text input.

### Features
- ✓ **Trie-based autocomplete** - Fast O(m) prefix matching
- ✓ **Frequency learning engine** - Adaptive ranking based on usage
- ✓ **Heap-based Top-K ranking** - Efficient suggestion ranking
- ✓ **Dynamic frequency updates** - Persist to disk immediately
- ✓ **Sentence typing support** - Per-word suggestions
- ✓ **Tkinter GUI** - User-friendly interface
- ✓ **Analytics** - Frequency tracking and display
- ✓ **Levenshtein fuzzy matching** - Typo tolerance (bonus)
- ✓ **N-gram next-word prediction** - (bonus)
- ✓ **Atomic file operations** - Crash-safe persistence
- ✓ **Input normalization** - Lowercase handling
- ✓ **Comprehensive tests** - Full test coverage

### Requirements
- Python 3.10+
- tkinter (included with Python)
- No external packages required

### Installation & Quick Start

```bash
# Navigate to project
cd "Bilingual-Predictive-Text-Autocomplete-System-English-Romanized-Nepali-"

# Run the application
python main.py

# Or run tests
python test_romanized_nepali.py
```

### How It Works

**Example: User types "k"**
```
1. Input: "k"
2. System extracts last word: "k"
3. Trie finds matches: ["k_cha", "ke_gardai"]
4. Ranker sorts by frequency: ["k_cha" (90), "ke_gardai" (0)]
5. GUI displays suggestions
6. User double-clicks "k_cha"
7. Text becomes: "k_cha "
8. Frequency of "k_cha" updated: 90 → 91
9. Changes persisted to data/frequency.json
```

**Example: Sentence typing "how are you"**
```
Type "how " → suggestions for "how"
Type "are " → suggestions for "are" (not "how")
Type "you" → suggestions for "you"

Each word typed gets its own suggestions!
```

### Key Implementation Details

#### 1. **Frequency Engine** (`core/frequency.py`)
- Loads/saves word frequencies from JSON
- **Atomic writes**: temp file + rename (prevents corruption)
- **Auto-persistence**: saves immediately after each update
- **Error recovery**: gracefully handles corrupted JSON
- **Normalization**: all words stored lowercase

#### 2. **Trie Data Structure** (`core/trie.py`)
- O(1) insertion per character
- O(m) search for word of length m
- Fast prefix matching for autocomplete

#### 3. **Ranking Algorithm** (`core/ranker.py`)
- Heap-based Top-K ranking: O(n log k)
- Higher frequency = higher ranking
- Returns top 5 suggestions by default

#### 4. **GUI Application** (`gui/app.py`)
- Real-time suggestion updates
- Frequency scores displayed
- Double-click to select
- Enter to confirm
- Tab key disabled (prevents accidental inserts)
- Status bar for feedback

#### 5. **Dictionary Management** (`core/dataset.py`)
- Loads from `data/dictionary.txt`
- Removes duplicates automatically
- Handles romanization formats

### Data Files

**data/dictionary.txt** - Romanized Nepali words (one per line)
```
hello
hi
namaste
k_cha
```

**data/frequency.json** - Word usage statistics (auto-updated)
```json
{
    "hello": 120,
    "namaste": 45,
    "k_cha": 12
}
```

### GUI Controls

| Action | Result |
|--------|--------|
| Type character | Show suggestions for last word |
| Double-click suggestion | Insert word, update frequency |
| Press Enter | Confirm word, clear input |
| Press Tab | (Ignored - prevents accidental inserts) |

### File Structure
```
project/
├── main.py                          # Entry point
├── gui/app.py                       # GUI application
├── core/
│   ├── trie.py                      # Trie data structure
│   ├── dataset.py                   # Dictionary loader
│   ├── frequency.py                 # Frequency engine ⭐
│   ├── ranker.py                    # Ranking algorithm
│   ├── ngram.py                     # N-gram predictor
│   └── levenshtein.py              # Fuzzy matching
├── data/
│   ├── dictionary.txt              # Romanized Nepali words
│   └── frequency.json              # Word frequencies
├── test_romanized_nepali.py        # Comprehensive tests ⭐
├── IMPLEMENTATION.md               # Technical documentation ⭐
└── QUICKSTART.md                   # User guide ⭐
```

### Testing

Run comprehensive test suite:
```bash
python test_romanized_nepali.py
```

Tests verify:
- ✓ Dictionary loading
- ✓ Trie operations
- ✓ Frequency persistence
- ✓ Ranking algorithm
- ✓ Sentence handling
- ✓ Input normalization
- ✓ Full workflow

### Documentation

- **QUICKSTART.md** - User guide with examples
- **IMPLEMENTATION.md** - Technical implementation details

### Performance

| Operation | Complexity | Time |
|-----------|-----------|------|
| Load dictionary | O(n) | ~100ms for 1000 words |
| Prefix search | O(m + k) | ~1ms (m=prefix, k=results) |
| Ranking | O(n log k) | ~5ms for 100 suggestions |
| Update frequency | O(1) + I/O | ~10ms (includes file write) |

### Key Features Implemented

✓ **Modular Design**
- load_dictionary()
- load_frequency()
- update_frequency(word)
- get_suggestions(prefix)
- save_frequency()

✓ **Data Safety**
- Atomic file writes (temp + rename)
- Error recovery on corrupted files
- Auto-persistence after updates

✓ **User Experience**
- Real-time suggestions
- Frequency feedback
- Sentence support
- Clear status messages

✓ **Performance**
- Trie for O(m) search
- Heap for O(n log k) ranking
- Efficient memory usage

### Bonus Features

✓ Input normalization (lowercase)
✓ Duplicate word handling
✓ Levenshtein fuzzy matching
✓ N-gram prediction
✓ Analytics dashboard
✓ Atomic file operations
✓ Error recovery

### Example Workflow

```python
from gui.app import PredictiveTextGUI

# Create and run GUI
app = PredictiveTextGUI()
app.run()

# Or use programmatically:
from core.frequency import FrequencyEngine

freq = FrequencyEngine("data/frequency.json")
freq.update("namaste")           # Increase frequency by 1
print(freq.get("namaste"))       # Get current frequency
freq.update("namaste")           # Another increment
freq.save()                       # Persist to disk
```

### Future Enhancements

- [ ] Multi-language support
- [ ] User profiles with separate frequency
- [ ] Export/import functionality
- [ ] Advanced analytics
- [ ] Keyboard shortcuts configuration

---

**Status**: Complete and tested ✓

**Run with**: `python main.py`

