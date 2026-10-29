import React from 'react';

const ChatFeed = ({ messages, isLoading }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-900">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`flex ${
            msg.sender === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`max-w-2xl p-4 rounded-xl shadow-md ${
              msg.sender === 'user'
                ? 'bg-indigo-600 text-white rounded-br-none'
                : 'bg-slate-800 text-slate-100 border border-slate-700 rounded-bl-none'
            }`}
          >
            {/* Message Body */}
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {msg.text}
            </p>

            {/* Week 5: Source Attribution Badges */}
            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-3 pt-2 border-t border-slate-700/60 flex flex-wrap gap-1.5 items-center">
                <span className="text-[11px] font-semibold text-slate-400 mr-1">
                  Sources:
                </span>
                {msg.sources.map((src, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-950/80 text-indigo-300 border border-indigo-800/80"
                  >
                    📄 {src}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-slate-800 border border-slate-700 p-3 rounded-xl rounded-bl-none text-slate-400 text-xs animate-pulse">
            Ollama (llama3) is generating a response...
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatFeed;