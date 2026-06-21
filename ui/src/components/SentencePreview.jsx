import React from 'react';

export default function SentencePreview({ words }) {
  if (words.length === 0) {
    return (
      <div 
        className="w-full py-4 px-4 rounded-lg min-h-16 flex items-center"
        style={{ backgroundColor: '#141414', color: '#666666' }}
      >
        Start typing to compose your sentence...
      </div>
    );
  }

  return (
    <div 
      className="w-full py-4 px-4 rounded-lg min-h-16 flex flex-wrap gap-2 items-center"
      style={{ backgroundColor: '#141414' }}
    >
      {words.map((word, idx) => (
        <span
          key={idx}
          style={{
            color: idx === words.length - 1 ? '#afa9ec' : '#666666',
            fontWeight: idx === words.length - 1 ? '500' : '400'
          }}
          className="transition-colors"
        >
          {word}
          {idx < words.length - 1 && <span className="ml-1">|</span>}
        </span>
      ))}
    </div>
  );
}
