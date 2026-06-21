import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function WordList() {
  const [words, setWords] = useState([]);

  useEffect(() => {
    // Load first 8 words from the dictionary
    const loadDictionary = async () => {
      try {
        // Try to fetch from backend if available
        const response = await axios.get('/dictionary', {
          params: { limit: 8 }
        });
        const data = response.data;
        if (Array.isArray(data)) {
          setWords(data);
        } else {
          setWords([]);
        }
      } catch (error) {
        console.log('Dictionary endpoint not available, using fallback');
        // Fallback: show static sample data
        setWords([
          { word: 'namaste', freq: 152 },
          { word: 'dhanyavaad', freq: 98 },
          { word: 'gardai', freq: 87 },
          { word: 'huncha', freq: 76 },
          { word: 'timi', freq: 65 },
          { word: 'samma', freq: 54 },
          { word: 'bichara', freq: 43 },
          { word: 'paila', freq: 32 }
        ]);
      }
    };
    loadDictionary();
  }, []);

  if (!Array.isArray(words)) {
    return <div style={{ color: '#666666' }}>Loading...</div>;
  }

  return (
    <div 
      className="w-full h-full flex flex-col gap-3 overflow-y-auto"
      style={{ backgroundColor: '#0a0a0a' }}
    >
      <h3 style={{ color: '#afa9ec' }} className="font-semibold text-sm sticky top-0">
        Dictionary
      </h3>
      {words.map((item, idx) => (
        <div
          key={idx}
          style={{ backgroundColor: '#141414', borderColor: '#2a2a2a' }}
          className="p-2 border rounded text-sm"
        >
          <div style={{ color: '#ffffff' }} className="font-medium">
            {item.word}
          </div>
          <div style={{ color: '#666666' }} className="text-xs">
            freq: {item.freq}
          </div>
        </div>
      ))}
    </div>
  );
}
