import React from "react";
import AuthLogin from "./components/AuthLogin";
import AuthProfile from "./components/AuthProfile";
import AuthLogout from "./components/AuthLogout";
import AuthSignup from "./components/AuthSignup";

export default function App() {
  return (
    <>
      <AuthLogin></AuthLogin>
      <AuthLogout></AuthLogout>
      <AuthSignup></AuthSignup>
      <AuthProfile></AuthProfile>
    </>
  );
}
