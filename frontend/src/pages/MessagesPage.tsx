import React, { useState } from 'react';
import TabNavigation from '../components/TabNavigation';

interface Person {
  id: string;
  name: string;
  avatar: string;
  lastMessage: string;
}

interface Message {
  fromMe: boolean;
  text: string;
}

const mockPeople: Person[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    avatar: '👩🏻',
    lastMessage: 'See you at the Skytree! 😊',
  },
  {
    id: '2',
    name: 'Alex Rodriguez',
    avatar: '🧑🏽',
    lastMessage: 'Let’s grab sushi tomorrow!',
  },
  {
    id: '3',
    name: 'Emma Thompson',
    avatar: '👩🏼',
    lastMessage: 'Safe travels! ✈️',
  },
];

interface MessagesByPerson {
  [personId: string]: Message[];
}

const mockMessages: MessagesByPerson = {
  '1': [
    { fromMe: false, text: 'Hey Sarah! Are you joining the group tour?' },
    { fromMe: true, text: 'Yes! Looking forward to it.' },
    { fromMe: false, text: 'See you at the Skytree! 😊' },
  ],
  '2': [
    { fromMe: false, text: 'Let’s grab sushi tomorrow!' },
    { fromMe: true, text: 'Sounds great, Alex!' },
  ],
  '3': [
    { fromMe: false, text: 'Safe travels! ✈️' },
    { fromMe: true, text: 'Thanks Emma! You too.' },
  ],
};

const MessagesPage = () => {
  const [selectedPersonId, setSelectedPersonId] = useState<string>(
    mockPeople[0].id
  );
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<MessagesByPerson>(mockMessages);

  const selectedPerson = mockPeople.find((p) => p.id === selectedPersonId);
  const chat = messages[selectedPersonId] || [];

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages((prev) => ({
      ...prev,
      [selectedPersonId]: [
        ...(prev[selectedPersonId] || []),
        { fromMe: true, text: input },
      ],
    }));
    setInput('');
  };

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
              {mockPeople.map((person: Person) => (
                <button
                  key={person.id}
                  className={`w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-blue-900 transition ${
                    selectedPersonId === person.id ? 'bg-blue-900' : ''
                  }`}
                  onClick={() => setSelectedPersonId(person.id)}
                >
                  <span className="w-10 h-10 rounded-full bg-blue-700 flex items-center justify-center text-2xl">
                    {person.avatar}
                  </span>
                  <div className="flex-1">
                    <div className="font-semibold text-white">
                      {person.name}
                    </div>
                    <div className="text-xs text-gray-400 truncate">
                      {person.lastMessage}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </aside>
          {/* Chat Window */}
          <section className="flex-1 flex flex-col">
            <div className="p-4 border-b border-gray-700 flex items-center gap-3 bg-gray-900">
              <span className="w-10 h-10 rounded-full bg-blue-700 flex items-center justify-center text-2xl">
                {selectedPerson?.avatar}
              </span>
              <div className="font-bold text-white text-lg">
                {selectedPerson?.name}
              </div>
            </div>
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-900">
              {chat.map((msg: Message, idx: number) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.fromMe ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`px-4 py-2 rounded-2xl max-w-xs break-words ${
                      msg.fromMe
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-gray-800 text-gray-200 rounded-bl-none'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
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
          </section>
        </div>
      </main>
    </div>
  );
};

export default MessagesPage;
