import React, { useState } from 'react';
import TabNavigation from '../components/TabNavigation';

// Mock matches data
const mockMatches = [
  {
    id: '1',
    name: 'Sarah Chen',
    age: 24,
    location: 'San Francisco, CA',
    avatar: '👩🏻',
    bio: 'Recent grad exploring the world! Love food and photography 📸',
    commonActivities: ['Sushi at Tsukiji Market', 'Tokyo Skytree'],
    travelStyle: 'Cultural Immersion',
    rating: 4.9,
    tripOverlap: '2 days',
    interests: ['Photography', 'Street Food', 'Museums'],
  },
  {
    id: '2',
    name: 'Alex Rodriguez',
    age: 26,
    location: 'Austin, TX',
    avatar: '🧑🏽',
    bio: 'Adventure seeker and foodie. Always down for new experiences!',
    commonActivities: ['Shibuya Crossing', 'Harajuku Fashion'],
    travelStyle: 'Adventure Seeker',
    rating: 4.7,
    tripOverlap: '1 day',
    interests: ['Adventure', 'Nightlife', 'Local Cuisine'],
  },
  {
    id: '3',
    name: 'Emma Thompson',
    age: 23,
    location: 'London, UK',
    avatar: '👩🏼',
    bio: 'Solo traveler on a gap year. Love meeting new people and sharing stories!',
    commonActivities: ['Senso-ji Temple', 'Tokyo Skytree', 'Ramen Lunch'],
    travelStyle: 'Budget Backpacker',
    rating: 4.8,
    tripOverlap: '3 days',
    interests: ['Backpacking', 'Culture', 'Budget Travel'],
  },
];

// For now, mock trips (replace with prop or context in real app)
const mockTrips = [
  { id: 1, name: 'Summer in Spain' },
  { id: 2, name: 'Tokyo Adventure' },
];

const ConnectPage = () => {
  // Replace mockTrips with prop or context in real app
  const trips = mockTrips;
  const [selectedTripId, setSelectedTripId] = useState(
    trips.length > 0 ? trips[0].id : null
  );
  const [connectedUsers, setConnectedUsers] = useState<string[]>([]);
  const [savedUsers, setSavedUsers] = useState<string[]>([]);
  const [messageModalUser, setMessageModalUser] = useState<
    null | (typeof mockMatches)[0]
  >(null);
  const [messageText, setMessageText] = useState('');

  const connectWithUser = (userId: string) => {
    setConnectedUsers((prev) => [...prev, userId]);
  };
  const saveUser = (userId: string) => {
    setSavedUsers((prev) => [...prev, userId]);
  };
  const openMessageModal = (user: (typeof mockMatches)[0]) => {
    setMessageModalUser(user);
    setMessageText('');
  };
  const closeMessageModal = () => {
    setMessageModalUser(null);
    setMessageText('');
  };
  const sendMessage = () => {
    // For now, just close the modal. In a real app, send the message to backend.
    closeMessageModal();
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col">
      <TabNavigation activeTab="connect" />
      <main className="flex-1 flex flex-col items-center py-10 px-4">
        <div className="w-full max-w-4xl space-y-8">
          <div className="text-center space-y-4 pt-4">
            <div className="flex justify-center">
              <span className="text-4xl">🧑‍🤝‍🧑</span>
            </div>
            <h1 className="text-3xl font-bold text-white">
              Your Travel Matches
            </h1>
            <p className="text-gray-400">
              Connect with fellow travelers who share your itinerary
            </p>
          </div>

          {/* Trip Selector or Prompt */}
          {trips.length === 0 ? (
            <div className="flex flex-col items-center space-y-4 py-12">
              <div className="text-lg text-gray-300">
                You have no trips yet.
              </div>
              <a
                href="/trips"
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-full shadow-lg transition-all"
              >
                Create a Trip
              </a>
            </div>
          ) : (
            <div className="flex flex-col md:flex-row items-center gap-4 mb-8">
              <label className="text-blue-300 font-semibold">
                Select Trip:
              </label>
              <select
                className="bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                value={selectedTripId ?? ''}
                onChange={(e) => setSelectedTripId(Number(e.target.value))}
              >
                {trips.map((trip) => (
                  <option key={trip.id} value={trip.id}>
                    {trip.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Matches List */}
          {trips.length > 0 && (
            <div className="grid gap-6">
              {mockMatches.map((match) => (
                <div
                  key={match.id}
                  className="bg-gray-800/80 border border-gray-700 rounded-2xl shadow p-6 flex flex-col md:flex-row gap-6"
                >
                  <div className="flex flex-col items-center md:items-start w-24 flex-shrink-0">
                    <div className="w-16 h-16 rounded-full bg-blue-700 flex items-center justify-center text-3xl mb-2">
                      {match.avatar}
                    </div>
                    <div className="text-xs text-gray-400 text-center md:text-left">
                      {match.location}
                    </div>
                  </div>
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-xl font-bold text-white">
                          {match.name}
                        </h3>
                        <p className="text-gray-400 text-sm">
                          {match.age} • {match.location}
                        </p>
                      </div>
                      <div className="flex items-center space-x-1 text-yellow-400">
                        <span className="text-lg">★</span>
                        <span className="text-sm">{match.rating}</span>
                      </div>
                    </div>
                    <p className="text-gray-300">{match.bio}</p>
                    <div className="flex items-center gap-2 text-sm text-gray-400">
                      <span className="text-blue-300">🗓️</span>
                      <span>{match.tripOverlap} overlap</span>
                      <span className="bg-blue-900 text-blue-300 px-2 py-0.5 rounded-full text-xs font-semibold ml-2">
                        {match.travelStyle}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400 mb-1">
                        Common Activities:
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {match.commonActivities.map((activity, idx) => (
                          <span
                            key={idx}
                            className="bg-gray-700 text-gray-200 text-xs px-2 py-0.5 rounded-full"
                          >
                            {activity}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Interests:</p>
                      <div className="flex flex-wrap gap-1">
                        {match.interests.map((interest, idx) => (
                          <span
                            key={idx}
                            className="border border-gray-600 text-gray-200 text-xs px-2 py-0.5 rounded-full"
                          >
                            {interest}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="flex space-x-3 pt-2">
                      {connectedUsers.includes(match.id) ? (
                        <div className="flex items-center space-x-2">
                          <span className="bg-green-600 text-white px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                            🤝 Connected
                          </span>
                          <button
                            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-full text-xs font-semibold"
                            onClick={() => openMessageModal(match)}
                          >
                            💬 Message
                          </button>
                        </div>
                      ) : (
                        <button
                          onClick={() => connectWithUser(match.id)}
                          className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1"
                        >
                          🤝 Connect
                        </button>
                      )}
                      <button
                        onClick={() => saveUser(match.id)}
                        className={`border border-gray-600 text-gray-200 bg-transparent px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 ${
                          savedUsers.includes(match.id)
                            ? 'bg-blue-900 border-blue-600'
                            : ''
                        }`}
                      >
                        {savedUsers.includes(match.id) ? '💙 Saved' : '🤍 Save'}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
              {/* No More Matches Card */}
              <div className="bg-gray-800/60 border border-gray-700 rounded-2xl shadow p-8 text-center space-y-4">
                <div className="text-4xl text-gray-500">🧑‍🤝‍🧑</div>
                <h3 className="text-lg font-semibold text-white">
                  That's all for now!
                </h3>
                <p className="text-gray-400">
                  We'll notify you when more travelers with similar itineraries
                  are found.
                </p>
                <button className="border border-gray-600 text-gray-200 bg-transparent px-4 py-2 rounded-full text-sm font-semibold">
                  Set Match Preferences
                </button>
              </div>
            </div>
          )}
        </div>
        {/* Message Modal */}
        {messageModalUser && (
          <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="bg-gray-900 border border-blue-800 rounded-2xl shadow-2xl p-8 w-full max-w-md relative">
              <button
                className="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl"
                onClick={closeMessageModal}
                aria-label="Close"
              >
                &times;
              </button>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-full bg-blue-700 flex items-center justify-center text-2xl">
                  {messageModalUser.avatar}
                </div>
                <div>
                  <div className="font-bold text-lg text-white">
                    Message {messageModalUser.name}
                  </div>
                  <div className="text-gray-400 text-xs">
                    {messageModalUser.location}
                  </div>
                </div>
              </div>
              <textarea
                className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white mb-4"
                rows={4}
                placeholder="Type your message..."
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
              />
              <button
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-full shadow-lg transition-all w-full"
                onClick={sendMessage}
                disabled={!messageText.trim()}
              >
                Send
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ConnectPage;
