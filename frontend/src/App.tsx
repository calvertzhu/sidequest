import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import ProfilePage from "./pages/ProfilePage";
import TripsPage from "./pages/TripsPage";
import ConnectPage from "./pages/ConnectPage";
import MessagesPage from "./pages/MessagesPage";
import AuthLogin from "./components/AuthLogin";
import { useAuth0 } from "@auth0/auth0-react";
import api from "./api";

export default function App() {
  const { user, isAuthenticated, isLoading } = useAuth0();

  useEffect(() => {
    if (!isLoading) console.log(isLoading);
  }, [isLoading]);

  if (isLoading) {
    return <div>Loading...</div>;
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
