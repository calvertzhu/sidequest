import React from 'react';
import { Link } from 'react-router-dom';

const tabs = [
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'profile', label: 'Profile' },
  { key: 'trips', label: 'Trips' },
  { key: 'connect', label: 'Connect' },
  { key: 'messages', label: 'Messages' },
];

interface TabNavigationProps {
  activeTab: string;
}

const TabNavigation: React.FC<TabNavigationProps> = ({ activeTab }) => (
  <nav className="w-full bg-gray-950 border-b border-gray-800 shadow-lg sticky top-0 z-20">
    <div className="max-w-6xl mx-auto px-4 flex items-center h-16">
      <div className="font-extrabold text-2xl text-blue-400 tracking-tight mr-8 select-none">
        Sidequest
      </div>
      <div className="flex gap-2 md:gap-6 flex-1">
        {tabs.map((tab) => (
          <Link
            key={tab.key}
            to={tab.key === 'dashboard' ? '/' : `/${tab.key}`}
            className={`px-4 py-2 rounded-md font-medium transition-colors text-sm md:text-base
              ${
                activeTab === tab.key
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-blue-400'
              }`}
          >
            {tab.label}
          </Link>
        ))}
      </div>
    </div>
  </nav>
);

export default TabNavigation;
