import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import ProfilePage from "./pages/ProfilePage";
import TripsPage from "./pages/TripsPage";
import ConnectPage from "./pages/ConnectPage";
import MessagesPage from "./pages/MessagesPage";
import AuthLogin from "./components/AuthLogin";

export default function App() {
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
