import React from 'react';

const Sidebar = ({ conversations, activeId, onSelectConversation, onNewChat }) => {
  return (
    <div className="w-64 bg-slate-950 border-r border-slate-800 p-4 flex flex-col h-full text-slate-300">
      <button
        onClick={onNewChat}
        className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2 px-4 rounded-lg text-sm font-medium mb-4 transition"
      >
        + New Chat
      </button>
      <div className="flex-1 overflow-y-auto space-y-1">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 px-2">
          History
        </p>
        {conversations.map((conv, index) => {
          const convId = conv.conversation_id || conv.id || `conv_${index}`;
          const isSelected = activeId === convId;

          return (
            <button
              key={convId}
              onClick={() => onSelectConversation(convId)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm truncate transition-colors ${
                isSelected
                  ? 'bg-indigo-600 text-white font-medium'
                  : 'hover:bg-slate-900 text-slate-300 bg-slate-900/50'
              }`}
            >
              {conv.title || 'Untitled Conversation'}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default Sidebar;