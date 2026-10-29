import React, { useState, useEffect } from 'react';
import ChatFeed from './components/ChatFeed';
import ChatInput from './components/ChatInput';
import Sidebar from './components/Sidebar';
import AdminDashboard from './components/AdminDashboard';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(`session_${Date.now()}`);

  // Fetch list of saved conversations on mount
  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/history');
      if (res.ok) {
        const data = await res.json();
        setConversations(data.conversations || []);
      }
    } catch (err) {
      console.error('Failed to load conversation history list:', err);
    }
  };

  // Load past messages when selecting a session from Sidebar
  const handleSelectConversation = async (convId) => {
    setActiveConvId(convId);
    setIsLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/api/history/${convId}`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || []);
      }
    } catch (err) {
      console.error('Error fetching history:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Start a fresh conversation
  const handleNewChat = () => {
    const newId = `session_${Date.now()}`;
    setActiveConvId(newId);
    setMessages([]);
  };

  const handleSendMessage = async (userText) => {
    const updatedMessages = [...messages, { sender: 'user', text: userText }];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userText,
          conversation_id: activeConvId, // Pass active conversation ID
          stream: false
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessages([
          ...updatedMessages,
          {
            sender: 'bot',
            text: data.reply,
            sources: data.sources || []
          }
        ]);
        // Refresh conversation sidebar list
        fetchConversations();
      } else {
        setMessages([
          ...updatedMessages,
          { sender: 'bot', text: 'Error: ' + (data.error || 'Failed to fetch response.') }
        ]);
      }
    } catch (error) {
      setMessages([
        ...updatedMessages,
        { sender: 'bot', text: 'Connection error. Ensure Flask backend is running.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      <div className="flex flex-col w-64 border-r border-slate-800 bg-slate-950">
        <div className="p-4 flex gap-2 border-b border-slate-800">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex-1 py-1.5 px-3 rounded-lg text-xs font-semibold ${
              activeTab === 'chat' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
            }`}
          >
            Chat
          </button>
          <button
            onClick={() => setActiveTab('admin')}
            className={`flex-1 py-1.5 px-3 rounded-lg text-xs font-semibold ${
              activeTab === 'admin' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
            }`}
          >
            Admin Dashboard
          </button>
        </div>

        {activeTab === 'chat' && (
          <Sidebar
            conversations={conversations}
            activeId={activeConvId}
            onSelectConversation={handleSelectConversation}
            onNewChat={handleNewChat}
          />
        )}
      </div>

      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {activeTab === 'chat' ? (
          <>
            <header className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
              <h1 className="text-lg font-bold text-indigo-400 flex items-center gap-2">
                🤖 Enterprise AI Chatbot
              </h1>
              <span className="px-3 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-400 border border-emerald-800">
                ● API Connected
              </span>
            </header>

            {messages.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500">
                <span className="text-4xl mb-2">🤖</span>
                <p className="text-sm">Hello. How can I assist you today?</p>
              </div>
            ) : (
              <ChatFeed messages={messages} isLoading={isLoading} />
            )}

            <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
          </>
        ) : (
          <div className="flex-1 overflow-y-auto">
            <AdminDashboard />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;