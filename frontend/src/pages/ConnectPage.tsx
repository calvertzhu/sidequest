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
    id: 1,
    name: "Emma",
    age: 26,
    location: "San Francisco, CA",
    occupation: "Product Designer",
    education: "Stanford University",
    bio: "Love hiking, coffee, and good conversations. Looking for someone who shares my passion for adventure and creativity.",
    images: ["/placeholder.svg?height=600&width=400"],
    interests: ["Hiking", "Photography", "Coffee", "Travel", "Design"],
    distance: 2,
  },
  {
    id: 2,
    name: "Alex",
    age: 29,
    location: "San Francisco, CA",
    occupation: "Software Engineer",
    education: "UC Berkeley",
    bio: "Tech enthusiast by day, chef by night. Always up for trying new restaurants or cooking something delicious at home.",
    images: ["/placeholder.svg?height=600&width=400"],
    interests: ["Cooking", "Tech", "Gaming", "Fitness", "Music"],
    distance: 5,
  },
  {
    id: 3,
    name: "Sofia",
    age: 24,
    location: "San Francisco, CA",
    occupation: "Marketing Manager",
    education: "UCLA",
    bio: "Yoga instructor and marketing professional. Seeking balance in life and looking for someone who values mindfulness and growth.",
    images: ["/placeholder.svg?height=600&width=400"],
    interests: ["Yoga", "Meditation", "Reading", "Art", "Wellness"],
    distance: 3,
  },
  {
    id: 4,
    name: "Marcus",
    age: 31,
    location: "San Francisco, CA",
    occupation: "Architect",
    education: "MIT",
    bio: "Building dreams into reality. Love exploring the city's architecture and finding hidden gems. Weekend warrior on the basketball court.",
    images: ["/placeholder.svg?height=600&width=400"],
    interests: ["Architecture", "Basketball", "Travel", "Photography", "Wine"],
    distance: 7,
  },
];

export default function Component() {
  const [currentProfileIndex, setCurrentProfileIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationDirection, setAnimationDirection] = useState<
    "left" | "right" | null
  >(null);

  const currentProfile = sampleProfiles[currentProfileIndex];

  const handleSwipe = (direction: "left" | "right") => {
    if (isAnimating) return;

    setIsAnimating(true);
    setAnimationDirection(direction);

    setTimeout(() => {
      setCurrentProfileIndex((prev) => (prev + 1) % sampleProfiles.length);
      setIsAnimating(false);
      setAnimationDirection(null);
    }, 300);
  };

  const handleLike = () => handleSwipe("right");
  const handlePass = () => handleSwipe("left");

  if (!currentProfile) {
    return (
      <div className="from-gray-900 to-gray-800 min-h-screen text-white flex flex-col bg-cover bg-center">
        <TabNavigation activeTab="dashboard" />
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-pink-50 to-red-50">
          <div className="text-center">
            <Heart className="w-16 h-16 mx-auto mb-4 text-pink-500" />
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              No more profiles!
            </h2>
            <p className="text-gray-600">Check back later for more matches.</p>
          </div>
        </div>
      </div>
    );
  }

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

                  {/* Distance Badge */}
                  <div className="absolute top-4 right-4">
                    <Badge
                      variant="secondary"
                      className="bg-white/90 text-gray-800"
                    >
                      <MapPin className="w-3 h-3 mr-1" />
                      {currentProfile.distance} km away
                    </Badge>
                  </div>

                  {/* Basic Info Overlay */}
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <h2 className="text-3xl font-bold mb-1">
                      {currentProfile.name}, {currentProfile.age}
                    </h2>
                    <div className="flex items-center gap-4 text-sm opacity-90">
                      <div className="flex items-center gap-1">
                        <Briefcase className="w-4 h-4" />
                        {currentProfile.occupation}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Profile Details */}
                <div className="p-6 space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin className="w-4 h-4" />
                      <span className="text-sm">{currentProfile.location}</span>
                    </div>

                    <div className="flex items-center gap-2 text-gray-600">
                      <GraduationCap className="w-4 h-4" />
                      <span className="text-sm">
                        {currentProfile.education}
                      </span>
                    </div>
                  </div>

                  <p className="text-gray-700 text-sm leading-relaxed">
                    {currentProfile.bio}
                  </p>

                  {/* Interests */}
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-2 text-sm">
                      Interests
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {currentProfile.interests.map((interest, index) => (
                        <Badge
                          key={index}
                          variant="outline"
                          className="text-xs"
                        >
                          {interest}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center gap-6">
            <Button
              onClick={handlePass}
              size="lg"
              variant="outline"
              className="w-16 h-16 rounded-full border-2 border-gray-300 hover:border-red-400 hover:bg-red-50 transition-colors bg-transparent"
              disabled={isAnimating}
            >
              <X className="w-8 h-8 text-gray-600 hover:text-red-500" />
            </Button>

            <Button
              onClick={handleLike}
              size="lg"
              className="w-16 h-16 rounded-full bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 shadow-lg"
              disabled={isAnimating}
            >
              <Heart className="w-8 h-8 text-white fill-current" />
            </Button>
          </div>

          {/* Profile Counter */}
          <div className="text-center mt-6">
            <p className="text-sm text-gray-500">
              {currentProfileIndex + 1} of {sampleProfiles.length}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
