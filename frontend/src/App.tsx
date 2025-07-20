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

  const createUserifNotExists = async () => {
    var userExists;
    var userPosted;
    if (user != undefined) {
      userExists = await api.get(`/users/search?email=${user.email}`);

      if (!userExists.data.exists) {
        userPosted = await api.post("/users", {
          name: user.name,
          email: user.email,
          birthday: "1995-04-12",
          gender: "female",
          interests: ["books", "travel", "yoga"],
          profile_pic: "https://example.com/pics/sarah.jpg",
          dietary_restrictions: "vegetarian",
          location: "Toronto",
          travel_dates: {
            from: "2025-09-01",
            to: "2025-09-10",
          },
        });
      }
      console.log(userPosted);
    }
  };

  useEffect(() => {
    if (!isLoading) {
      createUserifNotExists();
    }
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
