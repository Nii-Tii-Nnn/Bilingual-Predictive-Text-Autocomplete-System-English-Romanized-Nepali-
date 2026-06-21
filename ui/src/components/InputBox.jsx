import React, { useState, useCallback } from 'react';
import axios from 'axios';

export default function InputBox({ value, onSuggestionsUpdate, onMatchCountUpdate, onInputChange }) {
  const [debounceTimer, setDebounceTimer] = useState(null);

  const fetchSuggestions = useCallback(async (prefix) => {
    if (!prefix.trim()) {
      onSuggestionsUpdate([]);
      onMatchCountUpdate(0);
      return;
    }

    try {
      const response = await axios.get('/suggest', {
        params: {
          prefix: prefix,
          limit: 6
        }
      });
      onSuggestionsUpdate(response.data || []);
      onMatchCountUpdate((response.data || []).length);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      onSuggestionsUpdate([]);
      onMatchCountUpdate(0);
    }
  }, [onSuggestionsUpdate, onMatchCountUpdate]);

  const handleChange = (e) => {
    const newValue = e.target.value;
    if (onInputChange) {
      onInputChange(newValue);
    }

    // Clear existing timer
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    // Set new timer for debounced fetch
    const timer = setTimeout(() => {
      fetchSuggestions(newValue);
    }, 150);

    setDebounceTimer(timer);
  };

  return (
    <div className="w-full">
      <input
        type="text"
        value={value}
        onChange={handleChange}
        placeholder="Type in romanized Nepali (e.g. gar)..."
        style={{
          backgroundColor: '#111111',
          borderColor: '#2a2a2a',
          color: '#ffffff'
        }}
        className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-500 transition-colors"
      />
    </div>
  );
}
