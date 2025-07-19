import React from 'react';

const testimonials = [
  {
    avatar: '🧑‍🎓',
    name: 'Alex G.',
    quote:
      'I made friends for life and saw places I never would have found on my own!',
  },
  {
    avatar: '🌍',
    name: 'Priya S.',
    quote: 'The AI itinerary was spot on. Every day was an adventure!',
  },
  {
    avatar: '🎒',
    name: 'Jordan T.',
    quote:
      'Perfect for solo travelers. I never felt alone and always had something fun to do.',
  },
];

const Testimonials = () => (
  <section className="py-16 px-4 bg-gray-900">
    <h2 className="text-3xl md:text-4xl font-bold text-center mb-10 text-white">
      What Our Users Say
    </h2>
    <div className="flex flex-col md:flex-row justify-center items-stretch gap-8 max-w-4xl mx-auto">
      {testimonials.map((t, idx) => (
        <div
          key={idx}
          className="flex flex-col items-center bg-gray-800 rounded-xl p-8 shadow-lg w-full md:w-1/3"
        >
          <div className="text-5xl mb-4">{t.avatar}</div>
          <p className="text-gray-200 italic mb-4">“{t.quote}”</p>
          <div className="text-gray-400 font-semibold">{t.name}</div>
        </div>
      ))}
    </div>
  </section>
);

export default Testimonials;
