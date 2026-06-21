import React, { useState, useEffect } from 'react';
import InputBox from './components/InputBox';
import SuggestionRow from './components/SuggestionRow';
import SentencePreview from './components/SentencePreview';
import WordList from './components/WordList';
import StatusBar from './components/StatusBar';
import './index.css';

function App() {
  const [suggestions, setSuggestions] = useState([]);
  const [composedWords, setComposedWords] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [matchCount, setMatchCount] = useState(0);
  const [wordCount, setWordCount] = useState(0);
  const [isTrieReady, setIsTrieReady] = useState(true);
  const [languageMode, setLanguageMode] = useState('romanized');

  // Load dictionary word count on mount
  useEffect(() => {
    const estimateWordCount = async () => {
      try {
        const response = await fetch('/dictionary-count');
        const data = await response.json();
        setWordCount(data.count || 0);
      } catch (error) {
        // Fallback: assume ~15000 words (typical for Nepali dictionary)
        setWordCount(15000);
      }
    };
    estimateWordCount();
  }, []);

  const handleSuggestionsUpdate = (newSuggestions) => {
    setSuggestions(newSuggestions);
  };

  const handleMatchCountUpdate = (count) => {
    setMatchCount(count);
  };

  const handleInputChange = (value) => {
    setInputValue(value);
  };

  const handleSelectSuggestion = (word) => {
    setComposedWords([...composedWords, word]);
    setInputValue('');
    setSuggestions([]);
    setMatchCount(0);
  };

  const handleClearSentence = () => {
    setComposedWords([]);
    setInputValue('');
    setSuggestions([]);
    setMatchCount(0);
  };

  // macOS-style traffic light dots
  const TrafficLights = () => (
    <div className="flex gap-2">
      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ff5f57' }} />
      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ffbd2e' }} />
      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#28c940' }} />
    </div>
  );

  return (
    <div className="w-screen h-screen flex flex-col" style={{ backgroundColor: '#0a0a0a' }}>
      {/* Header */}
      <div 
        className="flex items-center justify-between px-4 py-3 border-b"
        style={{ 
          backgroundColor: '#0a0a0a',
          borderColor: '#2a2a2a'
        }}
      >
        <TrafficLights />
        <h1 
          className="text-lg font-semibold"
          style={{ color: '#afa9ec' }}
        >
          Nepali Autocomplete
        </h1>
        <button
          onClick={() => setLanguageMode(mode => mode === 'romanized' ? 'unicode' : 'romanized')}
          style={{
            backgroundColor: '#1a1a1a',
            borderColor: '#534ab7',
            color: '#afa9ec'
          }}
          className="px-3 py-1 border rounded text-sm font-medium hover:opacity-80 transition-opacity"
        >
          {languageMode === 'romanized' ? 'Romanized' : 'Unicode'}
        </button>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <div 
          className="w-48 border-r overflow-y-auto p-4"
          style={{ 
            backgroundColor: '#0a0a0a',
            borderColor: '#2a2a2a'
          }}
        >
          <WordList />
        </div>

        {/* Center Main Content */}
        <div className="flex-1 flex flex-col p-6 overflow-y-auto gap-6">
          {/* Input Section */}
          <div className="space-y-3">
            <label style={{ color: '#afa9ec' }} className="block text-sm font-semibold">
              Input
            </label>
            <InputBox 
              value={inputValue}
              onSuggestionsUpdate={handleSuggestionsUpdate}
              onMatchCountUpdate={handleMatchCountUpdate}
              onInputChange={handleInputChange}
            />
          </div>

          {/* Suggestions Section */}
          <div className="space-y-3">
            <label style={{ color: '#afa9ec' }} className="block text-sm font-semibold">
              Suggestions ({matchCount})
            </label>
            <SuggestionRow 
              suggestions={suggestions}
              onSelect={handleSelectSuggestion}
              inputValue={inputValue}
            />
          </div>

          {/* Sentence Preview Section */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label style={{ color: '#afa9ec' }} className="block text-sm font-semibold">
                Sentence ({composedWords.length} words)
              </label>
              {composedWords.length > 0 && (
                <button
                  onClick={handleClearSentence}
                  style={{
                    backgroundColor: '#1a1a1a',
                    borderColor: '#534ab7',
                    color: '#afa9ec'
                  }}
                  className="px-2 py-1 border rounded text-xs hover:opacity-80 transition-opacity"
                >
                  Clear
                </button>
              )}
            </div>
            <SentencePreview words={composedWords} />
          </div>
        </div>
      </div>

      {/* Status Bar */}
      <StatusBar 
        wordCount={wordCount}
        matchCount={matchCount}
        isTrieReady={isTrieReady}
      />
    </div>
  );
}

export default App;
