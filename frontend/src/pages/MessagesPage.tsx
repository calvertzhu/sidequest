import React, { useEffect, useState } from 'react';
import TabNavigation from '../components/TabNavigation';
import { useAuth0 } from '@auth0/auth0-react';
import api from '../api';

type SavedUser = { id: string; name: string };
type Message = {
  from_user_id: string;
  to_user_id: string;
  text: string;
  created_at: string;
};

const MessagesPage = () => {
  const { user } = useAuth0();
  const myUserId = user?.sub || user?.email;
  const [savedUsers, setSavedUsers] = useState<SavedUser[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  // Load saved users
  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem('savedUsers') || '[]');
    setSavedUsers(saved);
  }, []);

  // Load messages for selected user from backend
  useEffect(() => {
    if (selectedUserId && myUserId) {
      api.get(`/messages/${myUserId}/${selectedUserId}`).then((res) => {
        setMessages(res.data);
      });
    }
  }, [selectedUserId, myUserId]);

  // Send a message to backend
  const sendMessage = async () => {
    if (!input.trim() || !selectedUserId || !myUserId) return;
    await api.post('/messages', {
      from_user_id: myUserId,
      to_user_id: selectedUserId,
      text: input,
    });
    setInput('');
    // Re-fetch messages
    api.get(`/messages/${myUserId}/${selectedUserId}`).then((res) => {
      setMessages(res.data);
    });
  };

  const selectedUser = savedUsers.find((u) => u.id === selectedUserId);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col">
      <TabNavigation activeTab="messages" />
      <main className="flex-1 flex flex-col items-center py-10 px-4">
        <div className="w-full max-w-5xl h-[70vh] bg-gray-900 rounded-2xl shadow-xl flex overflow-hidden">
          {/* People List */}
          <aside className="w-1/3 min-w-[200px] max-w-xs bg-gray-800 border-r border-gray-700 flex flex-col">
            <div className="p-4 text-blue-300 font-bold text-lg border-b border-gray-700">
              Messages
            </div>
            <div className="flex-1 overflow-y-auto">
              {savedUsers.length === 0 ? (
                <div className="text-gray-400 p-4">No saved users yet.</div>
              ) : (
                <ul>
                  {savedUsers.map((user) => (
                    <li
                      key={user.id}
                      className={`p-4 border-b border-gray-700 text-white cursor-pointer hover:bg-blue-900 transition ${
                        selectedUserId === user.id ? 'bg-blue-900' : ''
                      }`}
                      onClick={() => setSelectedUserId(user.id)}
                    >
                      {user.name}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </aside>
          {/* Chat Window */}
          <section className="flex-1 flex flex-col">
            {selectedUser ? (
              <>
                <div className="p-4 border-b border-gray-700 flex items-center gap-3 bg-gray-900">
                  <div className="font-bold text-white text-lg">
                    {selectedUser.name}
                  </div>
                </div>
                <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-900">
                  {messages.length === 0 ? (
                    <div className="text-gray-400">No messages yet.</div>
                  ) : (
                    messages.map((msg, idx) => (
                      <div
                        key={idx}
                        className={`flex ${
                          msg.from_user_id === myUserId
                            ? 'justify-end'
                            : 'justify-start'
                        }`}
                      >
                        <div
                          className={`px-4 py-2 rounded-2xl max-w-xs break-words ${
                            msg.from_user_id === myUserId
                              ? 'bg-blue-600 text-white rounded-br-none'
                              : 'bg-gray-800 text-gray-200 rounded-bl-none'
                          }`}
                        >
                          {msg.text}
                        </div>
                      </div>
                    ))
                  )}
                </div>
                <form
                  className="p-4 border-t border-gray-700 bg-gray-900 flex gap-2"
                  onSubmit={(e) => {
                    e.preventDefault();
                    sendMessage();
                  }}
                >
                  <input
                    className="flex-1 bg-gray-800 border border-gray-700 rounded-full px-4 py-2 text-white focus:outline-none"
                    placeholder="Type a message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                  />
                  <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 rounded-full shadow-lg transition-all"
                    disabled={!input.trim()}
                  >
                    Send
                  </button>
                </form>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center text-gray-400">
                Select a user to start messaging.
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
};

export default MessagesPage;
