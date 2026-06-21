import React, { useState, useEffect } from 'react';

export default function StatusBar({ wordCount, matchCount, isTrieReady }) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div 
      className="w-full px-4 py-2 flex items-center justify-between text-xs border-t"
      style={{ 
        backgroundColor: '#0a0a0a',
        borderColor: '#2a2a2a',
        color: '#666666'
      }}
    >
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div 
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: isTrieReady ? '#4ade80' : '#ef4444' }}
          />
          <span>{isTrieReady ? 'Trie ready' : 'Loading...'}</span>
        </div>
        <span>Words: {wordCount}</span>
        <span>Matches: {matchCount}</span>
      </div>
      <div>{time}</div>
    </div>
  );
}
