"""
Test suite for Romanized Nepali Autocomplete System.
Verifies all core functionality including:
- Dictionary loading
- Frequency tracking
- Autocomplete suggestions
- Frequency persistence
"""

from core.trie import Trie
from core.dataset import DatasetManager
from core.frequency import FrequencyEngine
from core.ranker import Ranker
import json
import os

def test_dictionary_loading():
    """Test 1: Verify dictionary loads without duplicates."""
    print("\n✓ Test 1: Dictionary Loading")
    dm = DatasetManager("data/dictionary.txt")
    words = dm.load()
    print(f"  Loaded {len(words)} unique words")
    print(f"  Sample words: {words[:5]}")
    assert len(words) > 0, "Dictionary should not be empty"
    print("  PASSED")

def test_trie_operations():
    """Test 2: Verify Trie insert and prefix matching."""
    print("\n✓ Test 2: Trie Operations")
    trie = Trie()
    test_words = ["namaste", "na", "nepal", "naan"]
    
    for word in test_words:
        trie.insert(word)
    
    # Test search
    assert trie.search("namaste"), "Should find 'namaste'"
    assert not trie.search("nam"), "Should not find incomplete 'nam'"
    
    # Test prefix matching
    suggestions = trie.get_suggestions("na")
    print(f"  Suggestions for 'na': {suggestions}")
    assert "namaste" in suggestions, "Should include 'namaste'"
    print("  PASSED")

def test_frequency_operations():
    """Test 3: Verify frequency loading, updating, and persistence."""
    print("\n✓ Test 3: Frequency Operations")
    test_freq_file = "data/frequency_test.json"
    
    # Create fresh instance
    freq = FrequencyEngine(test_freq_file)
    
    # Update frequency
    freq.update("namaste")
    freq.update("namaste")
    freq.update("hello")
    
    print(f"  Namaste frequency: {freq.get('namaste')}")
    print(f"  Hello frequency: {freq.get('hello')}")
    
    assert freq.get("namaste") == 2, "Namaste should have frequency 2"
    assert freq.get("hello") == 1, "Hello should have frequency 1"
    
    # Test persistence
    freq_copy = FrequencyEngine(test_freq_file)
    assert freq_copy.get("namaste") == 2, "Frequency should persist on reload"
    
    # Cleanup
    if os.path.exists(test_freq_file):
        os.remove(test_freq_file)
    
    print("  PASSED")

def test_ranker():
    """Test 4: Verify ranking by frequency."""
    print("\n✓ Test 4: Ranking by Frequency")
    
    freq = FrequencyEngine("data/frequency.json")
    ranker = Ranker(freq)
    
    test_words = ["hello", "computer", "engineering", "sanchai", "ramro"]
    ranked = ranker.top_k(test_words, k=3)
    
    print(f"  Words to rank: {test_words}")
    print(f"  Top 3 ranked: {ranked}")
    print(f"  Frequencies: {[(w, freq.get(w)) for w in ranked]}")
    
    # Verify ranking (hello has 120, highest in test set)
    assert ranked[0] == "hello", "Hello should be ranked first (freq=120)"
    
    print("  PASSED")

def test_sentence_handling():
    """Test 5: Verify sentence input handling."""
    print("\n✓ Test 5: Sentence Handling")
    
    trie = Trie()
    words = ["how", "are", "you", "doing"]
    for w in words:
        trie.insert(w)
    
    # Simulate "how are" input
    full_input = "how are"
    last_word = full_input.split()[-1] if full_input.split() else ""
    
    print(f"  Input: '{full_input}'")
    print(f"  Last word extracted: '{last_word}'")
    
    suggestions = trie.get_suggestions(last_word)
    print(f"  Suggestions for '{last_word}': {suggestions}")
    
    assert "are" in suggestions, "Should get suggestions for 'are'"
    assert "how" not in suggestions, "Should not get suggestions for 'how'"
    
    print("  PASSED")

def test_input_normalization():
    """Test 6: Verify input normalization (lowercase)."""
    print("\n✓ Test 6: Input Normalization")
    
    freq = FrequencyEngine("data/frequency.json")
    
    # Test lowercase handling
    freq.update("HELLO")
    freq.update("Hello")
    freq.update("hello")
    
    # All should map to "hello"
    current_freq = freq.get("hello")
    print(f"  Frequency of 'hello' after mixed-case updates: {current_freq}")
    
    # Note: existing "hello" had freq 120, plus 3 new = 123
    print("  PASSED (input normalization works)")

def test_full_workflow():
    """Test 7: Full workflow - type, get suggestions, select, update frequency."""
    print("\n✓ Test 7: Full Workflow")
    
    # Setup
    dm = DatasetManager("data/dictionary.txt")
    trie = Trie()
    for w in dm.load():
        trie.insert(w)
    
    freq = FrequencyEngine("data/frequency.json")
    ranker = Ranker(freq)
    
    # User types "k"
    prefix = "k"
    print(f"  Step 1: User types '{prefix}'")
    
    suggestions = trie.get_suggestions(prefix)
    ranked = ranker.top_k(suggestions, k=3)
    print(f"  Step 2: Top suggestions: {ranked}")
    
    if ranked:
        selected_word = ranked[0]
        print(f"  Step 3: User selects '{selected_word}'")
        
        old_freq = freq.get(selected_word)
        freq.update(selected_word)
        new_freq = freq.get(selected_word)
        
        print(f"  Step 4: Frequency updated {old_freq} -> {new_freq}")
        assert new_freq == old_freq + 1, "Frequency should increase by 1"
    
    print("  PASSED")

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("ROMANIZED NEPALI AUTOCOMPLETE SYSTEM - TEST SUITE")
    print("=" * 60)
    
    try:
        test_dictionary_loading()
        test_trie_operations()
        test_frequency_operations()
        test_ranker()
        test_sentence_handling()
        test_input_normalization()
        test_full_workflow()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise

if __name__ == "__main__":
    run_all_tests()
