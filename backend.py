from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.trie import Trie
from core.ranker import Ranker
from core.frequency import FrequencyEngine

app = Flask(__name__)
CORS(app)

# Initialize data structures
trie = None
ranker = None
freq_engine = None
word_count = 0

def initialize_backend():
    """Initialize Trie, Ranker, and frequency data"""
    global trie, ranker, freq_engine, word_count
    
    try:
        # Initialize frequency engine
        frequency_path = os.path.join(os.path.dirname(__file__), 'data', 'frequency.json')
        freq_engine = FrequencyEngine(frequency_path)
        
        # Initialize Trie
        trie = Trie()
        dict_path = os.path.join(os.path.dirname(__file__), 'data', 'dictionary.txt')
        
        with open(dict_path, 'r', encoding='utf-8') as f:
            words = f.read().strip().split('\n')
            for word in words:
                word = word.strip()
                if word:
                    trie.insert(word)
            word_count = len([w for w in words if w.strip()])
        
        # Initialize Ranker with frequency engine
        ranker = Ranker(freq_engine)
        
        print(f"✓ Backend initialized: {word_count} words loaded")
        return True
    except Exception as e:
        print(f"✗ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/suggest', methods=['GET'])
def suggest():
    """Get suggestions for a given prefix"""
    prefix = request.args.get('prefix', '').strip()
    limit = int(request.args.get('limit', 6))
    
    if not prefix:
        return jsonify([])
    
    if not trie:
        return jsonify({'error': 'Backend not initialized'}), 500
    
    try:
        # Get all words with this prefix
        words = trie.get_suggestions(prefix)
        
        # Rank by frequency
        ranked = ranker.top_k(words, limit)
        
        # Format response with frequency scores
        result = []
        for word in ranked:
            freq = freq_engine.get(word)
            result.append({'word': word, 'freq': freq})
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in /suggest: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Simple landing page for the backend root URL."""
    return jsonify({
        'status': 'ok',
        'message': 'Flask backend is running',
        'endpoints': ['/health', '/suggest', '/dictionary-count', '/dictionary']
    })

@app.route('/dictionary-count', methods=['GET'])
def dictionary_count():
    """Get total word count in dictionary"""
    return jsonify({'count': word_count})

@app.route('/dictionary', methods=['GET'])
def dictionary():
    """Get first N words from dictionary with frequency"""
    limit = int(request.args.get('limit', 8))
    
    try:
        dict_path = os.path.join(os.path.dirname(__file__), 'data', 'dictionary.txt')
        with open(dict_path, 'r', encoding='utf-8') as f:
            words = [w.strip() for w in f.read().strip().split('\n') if w.strip()][:limit]
        
        result = []
        for word in words:
            freq = freq_engine.get(word)
            result.append({'word': word, 'freq': freq})
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in /dictionary: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'trie_ready': trie is not None,
        'word_count': word_count
    })

if __name__ == '__main__':
    if initialize_backend():
        print("Starting Flask server on http://localhost:5000")
        app.run(debug=True, port=5000, host='localhost')
    else:
        print("Failed to initialize backend")
        sys.exit(1)
