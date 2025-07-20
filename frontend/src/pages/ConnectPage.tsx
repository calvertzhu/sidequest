"use client";

import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Heart, X, MapPin, Briefcase, GraduationCap } from "lucide-react";
import TabNavigation from "../components/TabNavigation";

interface Profile {
  id: number;
  name: string;
  age: number;
  location: string;
  occupation: string;
  education: string;
  bio: string;
  images: string[];
  interests: string[];
  distance: number;
}

const sampleProfiles: Profile[] = [
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
    <div className="from-gray-900 to-gray-800 min-h-screen text-white flex flex-col bg-cover bg-center">
      <TabNavigation activeTab="dashboard" />
      <div className="min-h-screen bg-gradient-to-br from-pink-50 to-red-50 p-4">
        <div className="max-w-sm mx-auto">
          {/* Header */}
          <div className="flex items-center justify-center mb-6 pt-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-red-500 rounded-full flex items-center justify-center">
                <Heart className="w-5 h-5 text-white fill-current" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-red-500 bg-clip-text text-transparent">
                Spark
              </h1>
            </div>
          </div>

          {/* Profile Card */}
          <div className="relative mb-6">
            <Card
              className={`overflow-hidden shadow-2xl transition-all duration-300 ${
                isAnimating
                  ? animationDirection === "right"
                    ? "transform translate-x-full rotate-12 opacity-0"
                    : "transform -translate-x-full -rotate-12 opacity-0"
                  : "transform translate-x-0 rotate-0 opacity-100"
              }`}
            >
              <CardContent className="p-0">
                {/* Profile Image */}
                <div className="relative">
                  <img
                    src={currentProfile.images[0] || "/placeholder.svg"}
                    alt={currentProfile.name}
                    className="w-full h-96 object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

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
}
