import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ProfilePage from './pages/ProfilePage';
import TripsPage from './pages/TripsPage';
import ConnectPage from './pages/ConnectPage';
import MessagesPage from './pages/MessagesPage';
import AuthLogin from './components/AuthLogin';
import ProfileSetup from './components/ProfileSetup';
import { useAuth0 } from '@auth0/auth0-react';
import api from './api';

export default function App() {
  const { user, isAuthenticated, isLoading } = useAuth0();
  const [showProfileSetup, setShowProfileSetup] = useState(false);
  const [isCheckingUser, setIsCheckingUser] = useState(true);
  const [userCheckComplete, setUserCheckComplete] = useState(false);

  const checkUserAndSetup = async () => {
    if (user && isAuthenticated) {
      try {
        // Check if user exists in our database
        const response = await api.get(`/users/search?email=${user.email}`);
        console.log('User check response:', response.data);

        if (response.data.exists) {
          // User exists, continue to normal app
          setShowProfileSetup(false);
        } else {
          // User doesn't exist, show profile setup
          setShowProfileSetup(true);
        }
      } catch (error) {
        console.error('Error checking user:', error);
        // If there's an error, don't assume user doesn't exist
        // Instead, show the normal app and let the user navigate
        setShowProfileSetup(false);
      }
    }
    setIsCheckingUser(false);
    setUserCheckComplete(true);
  };

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      checkUserAndSetup();
    } else if (!isLoading && !isAuthenticated) {
      // Reset states when user is not authenticated (logout)
      setIsCheckingUser(false);
      setUserCheckComplete(true);
      setShowProfileSetup(false);
    }
  }, [isLoading, isAuthenticated, user]);

  if (
    isLoading ||
    (isAuthenticated && (isCheckingUser || !userCheckComplete))
  ) {
    return (
      <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  // Show profile setup for new users only when we're certain they don't exist
  if (showProfileSetup && isAuthenticated && user && userCheckComplete) {
    return <ProfileSetup />;
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/trips" element={<TripsPage />} />
        <Route path="/connect" element={<ConnectPage />} />
        <Route path="/messages" element={<MessagesPage />} />
        <Route path="/login" element={<AuthLogin />} />
      </Routes>
    </Router>
  );
}
