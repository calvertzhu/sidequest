<<<<<<< HEAD
import { useAuth0 } from '@auth0/auth0-react';
import React from 'react';
import { Link } from 'react-router-dom';

const tabs = [
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'profile', label: 'Profile' },
  { key: 'trips', label: 'Trips' },
  { key: 'connect', label: 'Connect' },
  { key: 'messages', label: 'Messages' },
=======
import { useAuth0 } from "@auth0/auth0-react";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const initialTabs = [
  { key: "dashboard", label: "Dashboard" },
  { key: "profile", label: "Profile" },
  { key: "trips", label: "Trips" },
  { key: "connect", label: "Connect" },
  { key: "messages", label: "Messages" },
>>>>>>> 5fd33141ee3fb75a8acadbf8f736799cc2a11055
];

interface TabNavigationProps {
  activeTab: string;
}

const TabNavigation: React.FC<TabNavigationProps> = ({ activeTab }) => {
  const [tabs, setTabs] = useState(initialTabs);
  const { loginWithRedirect, isAuthenticated, logout } = useAuth0();

  useEffect(() => {
    if (!isAuthenticated) {
      setTabs([{ key: "dashboard", label: "Dashboard" }]);
    } else {
      setTabs(initialTabs);
    }
  }, [isAuthenticated]);

  return (
    <div className="flex items-center bg-gray-950 border-b border-gray-800 shadow-lg sticky top-0 z-20">
      <div className="flex-1 mx-auto px-4 flex items-center h-16">
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

      <div className="mr-4 mx-auto flex justify-center">
        {isAuthenticated ? (
          <div
            onClick={() =>
              logout({ logoutParams: { returnTo: window.location.origin } })
            }
            className="mr-3 p-3 bg-slate-200 text-black font-bold rounded-xl"
          >
            Logout
          </div>
        ) : (
          <>
            <div
              onClick={() => loginWithRedirect()}
              className="p-3 bg-slate-200 text-black font-bold rounded-xl"
            >
              Log In
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default TabNavigation;
