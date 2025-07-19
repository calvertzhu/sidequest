import React from 'react';

const features = [
  {
    icon: '🤖',
    title: 'AI-Powered Plans',
    desc: 'Get personalized itineraries crafted by smart algorithms.',
  },
  {
    icon: '🤝',
    title: 'Meet New Friends',
    desc: 'Connect with like-minded travelers and explore together.',
  },
  {
    icon: '🎉',
    title: 'Discover Local Events',
    desc: 'Find hidden gems, events, and activities wherever you go.',
  },
  {
    icon: '🛠️',
    title: 'Flexible Planning',
    desc: 'Let us plan for you, or customize your own adventure.',
  },
];

const Features = () => (
  <section className="py-16 px-4 bg-gradient-to-b from-gray-900 to-gray-800">
    <h2 className="text-3xl md:text-4xl font-bold text-center mb-10 text-white">
      Why Sidequest?
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
      {features.map((feature, idx) => (
        <div
          key={idx}
          className="flex items-start gap-4 bg-gray-800 rounded-xl p-6 shadow-lg"
        >
          <div className="text-4xl">{feature.icon}</div>
          <div>
            <h3 className="text-xl font-semibold text-white mb-1">
              {feature.title}
            </h3>
            <p className="text-gray-300">{feature.desc}</p>
          </div>
        </div>
      ))}
    </div>
  </section>
);

export default Features;
