import React from 'react';
import HeroSection from '../components/HeroSection';
import HowItWorks from '../components/HowItWorks';
import Features from '../components/Features';
import Testimonials from '../components/Testimonials';
import Footer from '../components/Footer';
import TabNavigation from '../components/TabNavigation';

const LandingPage = () => {
  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex flex-col">
      <TabNavigation activeTab="dashboard" />
      <main className="flex-1 flex flex-col">
        <HeroSection />
        <HowItWorks />
        <Features />
        <Testimonials />
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage;
