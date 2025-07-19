import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { Auth0Provider } from "@auth0/auth0-react";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Auth0Provider
      domain="dev-sslxwjos0zi4o1hx.us.auth0.com"
      clientId="hnykF9sjDYYFV868UdCMyxrjytmLe4CR"
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
      screen_hint="signup"
    >
      <App />
    </Auth0Provider>
  </StrictMode>
);
