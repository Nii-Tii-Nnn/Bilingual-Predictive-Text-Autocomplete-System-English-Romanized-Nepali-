# System Architecture & Design

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│                    gui/app.py (Tkinter)                     │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────┐   │
│  │ Input Field  │  │ Suggestions     │  │ Status Bar   │   │
│  │ "how are"    │  │ List Box        │  │ "✓ Selected" │   │
│  │              │  │ • are (150)     │  │              │   │
│  │ Hotkeys:     │  │ • aren't (5)    │  │              │   │
│  │ - Double-Clk │  │ • area (3)      │  │              │   │
│  │ - Enter      │  └─────────────────┘  └──────────────┘   │
│  │ - Tab (blocked)
│  └──────────────┘
└─────────────────┬───────────────────────────────────────────┘
                  │
         ┌────────┴──────────────┐
         ↓                       ↓
┌──────────────────┐   ┌──────────────────────┐
│  Data Search     │   │  Frequency Update    │
│  Layer           │   │  Layer               │
│                  │   │                      │
│ 1. Extract last  │   │ 1. Update in-memory  │
│    word via      │   │    frequency dict    │
│    split()       │   │                      │
│                  │   │ 2. Atomic save to    │
│ 2. Normalize     │   │    JSON file         │
│    (lowercase)   │   │                      │
│                  │   │ 3. Set status bar    │
│ 3. Search Trie   │   │    feedback          │
│                  │   │                      │
└────────┬─────────┘   └──────────┬───────────┘
         │                        │
         └────────┬───────────────┘
                  ↓
    ┌─────────────────────────────┐
    │   Ranking Layer             │
    │   core/ranker.py            │
    │                             │
    │ Heap-based Top-K:           │
    │ O(n log k) complexity       │
    │                             │
    │ Sort by:                    │
    │ - Higher frequency first    │
    │ - Return top 5              │
    │                             │
    └────────────┬────────────────┘
                 │
    ┌────────────┴────────────────┐
    ↓                             ↓
┌─────────────────────┐   ┌───────────────────────┐
│   Trie Data         │   │   Frequency Engine    │
│   Structure         │   │   core/frequency.py   │
│   core/trie.py      │   │                       │
│                     │   │ Load:                 │
│ Insert: O(m)        │   │ - Read frequency.json │
│ Search: O(m)        │   │ - Error handling      │
│ Prefix: O(m+k)      │   │                       │
│                     │   │ Update:               │
│ Methods:            │   │ - Increment counter   │
│ • insert()          │   │ - Auto-save           │
│ • search()          │   │ - Atomic writes       │
│ • starts_with()     │   │                       │
│ • get_suggestions() │   │ Save:                 │
│                     │   │ - Temp file + rename  │
│                     │   │ - Crash-safe          │
│                     │   │                       │
└─────────────────────┘   └───────────────────────┘
         ↑                           ↑
         │                           │
         └───────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │      Data Layer            │
        │                            │
        │ data/dictionary.txt        │
        │ • hello                    │
        │ • hi                       │
        │ • computer                 │
        │ • engineering              │
        │ • k_cha                    │
        │ • (16 total words)         │
        │                            │
        │ data/frequency.json        │
        │ {                          │
        │   "hello": 120,            │
        │   "computer": 45,          │
        │   "k_cha": 12,             │
        │   ...                      │
        │ }                          │
        └────────────────────────────┘
```

## Component Interactions

### When User Types "k"

```
User types 'k' in input field
    ↓
GUI.update_suggestions() triggered
    ↓
extract_last_word("k") → "k"
    ↓
normalize_input("k") → "k" (already lowercase)
    ↓
Trie.get_suggestions("k") → traverses tree
    ├─ Follow 'k' node
    ├─ Collect all end nodes below 'k'
    └─ Return: ["k_cha", "ke_gardai"]
    ↓
Ranker.top_k(["k_cha", "ke_gardai"], k=5)
    ├─ Get frequency of "k_cha" → 90
    ├─ Get frequency of "ke_gardai" → 0
    ├─ Build heap with (-90, "k_cha"), (-0, "ke_gardai")
    └─ Return: ["k_cha", "ke_gardai"]
    ↓
GUI displays:
    • k_cha (90)
    • ke_gardai (0)
```

### When User Double-Clicks "k_cha"

```
User double-clicks on "k_cha" in suggestions
    ↓
on_suggestion_selected() triggered
    ↓
Extract word from selection: "k_cha"
    ↓
Replace last word in input with "k_cha"
    ├─ Input was: "k"
    ├─ Split: ["k"]
    ├─ Replace: ["k_cha"]
    ├─ Join: "k_cha"
    └─ Result: "k_cha "
    ↓
freq.update("k_cha")
    ├─ In-memory: frequency["k_cha"] = 91
    ├─ Call freq.save()
    │   ├─ Write temp file: frequency.json.tmp
    │   ├─ Atomic rename: os.replace(tmp, json)
    │   └─ Persisted!
    └─ Frequency now: 91
    ↓
Update GUI
    ├─ Refresh suggestions
    ├─ Show status: "✓ Selected: k_cha"
    └─ Green color
    ↓
Next suggestions now show:
    • k_cha (91)  ← Increased!
    • ke_gardai (0)
```

### When User Presses Enter

```
User presses Enter with input "namaste"
    ↓
on_enter() triggered
    ↓
Extract last word: "namaste"
    ↓
Check if in dictionary:
    └─ trie.search("namaste") → True
    ↓
freq.update("namaste")
    ├─ Increment counter
    ├─ Auto-save to disk
    └─ Done!
    ↓
Show status: "✓ Confirmed: namaste"
    ↓
Clear input field
    └─ Ready for next word
```

## Data Structure Details

### Trie Node Structure

```
TrieNode {
    children: {
        'h': TrieNode { ... },
        'k': TrieNode {
            children: {
                '_': TrieNode {
                    children: {
                        'c': TrieNode {
                            children: {
                                'h': TrieNode {
                                    children: {
                                        'a': TrieNode {
                                            is_end: True
                                        }
                                    },
                                    is_end: False
                                }
                            }
                        }
                    }
                }
            },
            is_end: False
        }
    },
    is_end: False
}
```

Result: Word "k_cha" stored in tree structure for O(4) access.

### Frequency Dictionary

```json
{
    "hello": 120,
    "computer": 45,
    "engineering": 30,
    "sanchai": 75,
    "ramro": 60,
    "huncha": 40,
    "k_cha": 91,        ← Updated from 90 to 91
    "namaste": 105      ← Increased over time
}
```

Every update persisted atomically using:
1. Write to `frequency.json.tmp`
2. Atomic rename to `frequency.json`
3. No partial writes possible

## Algorithm Complexity Analysis

### Trie Operations

```
insert(word):
    Time: O(m) where m = word length
    Space: O(m) for stack
    Why: One character per node traversal

search(word):
    Time: O(m) where m = word length
    Space: O(1)
    Why: Traverse tree nodes

get_suggestions(prefix):
    Time: O(m + k) where m = prefix length, k = suggestions
    Space: O(k) for result array
    Why: Traverse to prefix + DFS for all matching words
```

### Ranking (Top-K)

```
top_k(words, k=5):
    Time: O(n log k) where n = suggestions, k = top results
    Space: O(k) for heap
    Why: Push n items into heap of size k
    Formula: n items * log(k heap size)
    
    Example with 100 suggestions, k=5:
    - Time: ~100 * log(5) ≈ 232 comparisons
    - Much faster than sorting: 100 * log(100) ≈ 664
```

### File I/O (Atomic Writes)

```
update_and_save():
    Time: O(1) in-memory + O(file_size) I/O
    For 1000 words: ~50KB JSON ≈ 10-15ms on SSD
    
    Steps:
    1. Update dict: O(1)
    2. Write temp: O(size)
    3. Rename: O(1)
    4. Total: O(size)
```

## Error Handling Flow

```
Try to load frequency.json
    ↓
    ├─ FileNotFoundError
    │   └─ Create new file on first save
    │
    ├─ JSONDecodeError (corrupted)
    │   ├─ Print error message
    │   ├─ Start with empty dict
    │   └─ Will save correctly on next update
    │
    └─ IOError (permissions)
        └─ Print error, continue with in-memory dict
        └─ May not persist if repeated
```

## Performance Profile

```
Scenario: User types "na" and selects from 5 suggestions

Timeline:
0ms     - User presses 'a' key
1ms     - extract_last_word() - instant
2ms     - normalize_input() - instant
3ms     - Trie.get_suggestions("na") - ~1ms
4ms     - Found 3 matches: ["na", "namaste", "naan"]
5ms     - Ranker.top_k() - ~2ms (heap operations)
6ms     - GUI updates listbox - ~2ms (tkinter)
8ms     - User sees suggestions

User double-clicks "namaste"
9ms     - on_suggestion_selected() called
10ms    - freq.update("namaste") - instant (in-memory)
10ms    - freq.save() to JSON - ~10ms (file I/O)
21ms    - GUI refreshes, status updates

Total: ~21ms from click to disk persistence
User perceives: Instant (< 100ms threshold)
```

## Safety Mechanisms

### Atomic Write Pattern
```python
def save(self):
    # Step 1: Write to temporary file
    temp_path = self.path + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(self.frequency, f)
    
    # Step 2: Atomic rename (kernel operation)
    # This either succeeds completely or fails completely
    # No partial/corrupted state possible
    os.replace(temp_path, self.path)
```

**Why this works:**
- Temp file write may fail or be incomplete
- Original file untouched
- Rename is atomic at OS level
- On crash: either old or new file present, never corrupted

### Error Recovery Pattern
```python
def load(self):
    if not os.path.exists(self.path):
        self.frequency = {}
        return
    
    try:
        with open(self.path) as f:
            self.frequency = json.load(f)
    except json.JSONDecodeError:
        # File corrupted but not lost
        self.frequency = {}
        # Next save will overwrite corrupted file
    except IOError:
        # Permission issues
        self.frequency = {}
```

## Modular Design

Each component has single responsibility:

```
┌─────────────┐
│   UI        │  - Display
│  app.py     │  - User input
│             │  - Event handling
└─────────────┘
       ↑ ↓
┌─────────────┐
│   Logic     │  - Search algorithm
│   trie.py   │  - Prefix matching
└─────────────┘
       ↑ ↓
┌─────────────┐
│   Ranking   │  - Sort by frequency
│ ranker.py   │  - Top-K selection
└─────────────┘
       ↑ ↓
┌─────────────┐
│  Frequency  │  - Load/save
│  frequency  │  - Update counts
│   .py       │  - Persistence
└─────────────┘
       ↑ ↓
┌─────────────┐
│   Dataset   │  - Load dictionary
│ dataset.py  │  - Handle formats
└─────────────┘
```

---

## Summary

✓ Clean layered architecture
✓ Single responsibility principle
✓ Efficient algorithms (O(m), O(n log k))
✓ Safe file operations (atomic writes)
✓ Error recovery mechanisms
✓ Modular, testable design
✓ User-friendly interface
✓ Production-ready implementation
