import React, { useState } from 'react';

const ChatInput = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;
    onSendMessage(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-slate-950 border-t border-slate-800 flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your question..."
        disabled={disabled}
        className="flex-1 bg-slate-800 text-white placeholder-slate-400 px-4 py-2.5 rounded-lg border border-slate-700 focus:outline-none focus:border-indigo-500 text-sm"
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition"
      >
        Send
      </button>
    </form>
  );
};

export default ChatInput;