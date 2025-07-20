import React from "react";

const steps = [
  {
    icon: "📝",
    title: "Create Your Profile",
    desc: "Tell us about yourself and your travel interests.",
  },
  {
    icon: "🗓️",
    title: "Enter Trip Details",
    desc: "Add your travel dates, budget, and preferences.",
  },
  {
    icon: "🌍",
    title: "Get Your Plan & Connect",
    desc: "Receive a custom itinerary and meet fellow travelers.",
  },
];

const HowItWorks = () => (
  <section className="bg-gray-900 py-16 px-4 bg-gray bg-gray-90">
    <h2 className="text-3xl md:text-4xl font-bold text-center mb-10 text-white">
      How It Works
    </h2>
    <div className="flex flex-col md:flex-row justify-center items-center gap-10 max-w-4xl mx-auto">
      {steps.map((step, idx) => (
        <div
          key={idx}
          className="flex flex-col items-center bg-gray-800 rounded-xl p-8 shadow-lg w-full md:w-1/3"
        >
          <div className="text-5xl mb-4">{step.icon}</div>
          <h3 className="text-xl font-semibold mb-2 text-white">
            {step.title}
          </h3>
          <p className="text-gray-300">{step.desc}</p>
        </div>
      ))}
    </div>
  </section>
);

export default HowItWorks;
