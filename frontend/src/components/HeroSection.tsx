import React from 'react';

const HeroSection = () => {
  return (
    <section className="flex flex-col items-center justify-center text-center py-24 px-4 bg-gradient-to-br from-blue-900 via-blue-800 to-gray-900">
      <h1 className="text-4xl md:text-6xl font-extrabold mb-4 tracking-tight text-white drop-shadow-lg">
        Travel Smarter. Connect Deeper.
      </h1>
      <p className="text-lg md:text-2xl mb-8 text-gray-300 max-w-2xl">
        Personalized itineraries, new friends, and unforgettable
        adventures—tailored just for you.
      </p>
      <div className="flex gap-4">
        <button className="bg-gradient-to-r from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700 text-white font-bold py-3 px-8 rounded-full shadow-lg transition-all text-lg">
          Get Started
        </button>
        <button className="bg-gray-800 border border-gray-600 text-gray-200 font-semibold py-3 px-8 rounded-full hover:bg-gray-700 transition-all text-lg">
          Learn More
        </button>
      </div>
    </section>
  );
};

export default HeroSection;
