import React, { useState } from 'react';
import TabNavigation from '../components/TabNavigation';

// Mock matches data
const mockMatches = [
  {
    id: '1',
    name: 'Sarah Chen',
    age: 24,
    gender: 'Female',
    location: 'San Francisco, CA',
    avatar: '👩🏻',
    commonActivities: ['Sushi at Tsukiji Market', 'Tokyo Skytree'],
    travelStyle: 'Cultural Immersion',
    tripOverlap: '2 days',
    interests: ['Photography', 'Street Food', 'Museums'],
  },
  {
    id: '2',
    name: 'Alex Rodriguez',
    age: 26,
    gender: 'Male',
    location: 'Austin, TX',
    avatar: '🧑🏽',
    commonActivities: ['Shibuya Crossing', 'Harajuku Fashion'],
    travelStyle: 'Adventure Seeker',
    tripOverlap: '1 day',
    interests: ['Adventure', 'Nightlife', 'Local Cuisine'],
  },
  {
    id: '3',
    name: 'Emma Thompson',
    age: 23,
    gender: 'Female',
    location: 'London, UK',
    avatar: '👩🏼',
    commonActivities: ['Senso-ji Temple', 'Tokyo Skytree', 'Ramen Lunch'],
    travelStyle: 'Budget Backpacker',
    tripOverlap: '3 days',
    interests: ['Backpacking', 'Culture', 'Budget Travel'],
  },
];

const mockTrips = [
  { id: 1, name: 'Summer in Spain' },
  { id: 2, name: 'Tokyo Adventure' },
];

const ConnectPage = () => {
  const trips = mockTrips;
  const [selectedTripId, setSelectedTripId] = useState(
    trips.length > 0 ? trips[0].id : null
  );
  const [currentIndex, setCurrentIndex] = useState(0);
  const [swipeDirection, setSwipeDirection] = useState<'left' | 'right' | null>(
    null
  );
  const [isAnimating, setIsAnimating] = useState(false);
  // Remove showCard state
  // const [showCard, setShowCard] = useState(true);

  const handleSwipe = (direction: 'left' | 'right') => {
    if (isAnimating) return;
    setIsAnimating(true);
    setSwipeDirection(direction);
    setTimeout(() => {
      setCurrentIndex((prev) => prev + 1);
      setSwipeDirection(null);
      setIsAnimating(false);
    }, 500);
  };

  const handleSkip = () => handleSwipe('left');
  const handleConnect = () => handleSwipe('right');

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

          {/* Card with Cross and Heart Buttons and Animation */}
          {trips.length > 0 && currentIndex < mockMatches.length && (
            <div className="flex flex-col items-center">
              <div
                className={`bg-gray-800/80 border border-gray-700 rounded-2xl shadow p-4 flex flex-col items-center w-80 mx-auto transition-all duration-500 ${
                  isAnimating
                    ? swipeDirection === 'left'
                      ? 'transform -translate-x-full -rotate-12 opacity-0'
                      : 'transform translate-x-full rotate-12 opacity-0'
                    : 'transform translate-x-0 rotate-0 opacity-100'
                }`}
              >
                <div className="w-16 h-16 rounded-full bg-blue-700 flex items-center justify-center text-3xl mb-2">
                  {mockMatches[currentIndex].avatar}
                </div>
                <h3 className="text-lg font-bold text-white text-center">
                  {mockMatches[currentIndex].name}
                </h3>
                <p className="text-gray-400 text-sm text-center">
                  {mockMatches[currentIndex].age} &bull;{' '}
                  {mockMatches[currentIndex].gender} &bull;{' '}
                  {mockMatches[currentIndex].location}
                </p>
                <div className="flex items-center justify-center gap-2 text-sm text-gray-400 w-full mt-2">
                  <span className="text-blue-300">🗓️</span>
                  <span>
                    {parseInt(mockMatches[currentIndex].tripOverlap)} days
                    overlap
                  </span>
                </div>
                <div className="w-full mt-2">
                  <p className="text-sm text-gray-400 mb-1 text-center">
                    Common Activities:
                  </p>
                  <div className="flex flex-wrap gap-1 justify-center">
                    {mockMatches[currentIndex].commonActivities.map(
                      (activity, idx) => (
                        <span
                          key={idx}
                          className="bg-gray-700 text-gray-200 text-xs px-2 py-0.5 rounded-full"
                        >
                          {activity}
                        </span>
                      )
                    )}
                  </div>
                </div>
                <div className="w-full mt-2">
                  <p className="text-sm text-gray-400 mb-1 text-center">
                    Interests:
                  </p>
                  <div className="flex flex-wrap gap-1 justify-center">
                    {mockMatches[currentIndex].interests.map(
                      (interest, idx) => (
                        <span
                          key={idx}
                          className="border border-gray-600 text-gray-200 text-xs px-2 py-0.5 rounded-full"
                        >
                          {interest}
                        </span>
                      )
                    )}
                  </div>
                </div>
                <div className="flex space-x-4 pt-4 justify-center">
                  <button
                    onClick={handleSkip}
                    className="border border-gray-500 text-white bg-transparent px-3 py-1 rounded-full text-lg flex items-center justify-center transition"
                    aria-label="Skip"
                    disabled={isAnimating}
                  >
                    ❌
                  </button>
                  <button
                    onClick={handleConnect}
                    className="border border-gray-300 text-white bg-transparent px-3 py-1 rounded-full text-lg flex items-center justify-center transition"
                    aria-label="Connect"
                    disabled={isAnimating}
                  >
                    ❤️
                  </button>
                </div>
              </div>
            </div>
          )}
          {currentIndex >= mockMatches.length && (
            <div className="text-center text-gray-400 mt-8">
              No more matches! We'll notify you when more travelers are found.
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default ConnectPage;
