import React from 'react';

export default function SuggestionRow({ suggestions, onSelect, inputValue }) {
  if (!inputValue.trim() || suggestions.length === 0) {
    return (
      <div className="w-full py-4 text-center" style={{ color: '#666666' }}>
        No suggestions available
      </div>
    );
  }

  return (
    <div className="w-full flex gap-2 flex-wrap">
      {suggestions.map((item, idx) => (
        <button
          key={idx}
          onClick={() => onSelect(item.word)}
          style={{
            backgroundColor: idx === 0 ? '#1a1a1a' : '#141414',
            borderColor: idx === 0 ? '#534ab7' : '#2a2a2a',
            color: idx === 0 ? '#afa9ec' : '#ffffff'
          }}
          className="px-3 py-2 border rounded-lg hover:opacity-80 transition-all active:scale-95 flex items-center gap-2"
        >
          <span className="font-medium">{item.word}</span>
          <span style={{ color: '#666666' }} className="text-xs">
            {item.freq}
          </span>
        </button>
      ))}
    </div>
  );
}
