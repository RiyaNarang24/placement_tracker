import { useEffect, useState } from "react";
import "./App.css";

import Auth from "./components/Auth";
import Dashboard from "./components/Dashboard";
import AddApplication from "./components/AddApplications";
import Navbar from "./components/Navbar";

function App() {
  const [token, setToken] = useState(
    () => localStorage.getItem("token") || ""
  );

  const [username, setUsername] = useState(
    () => localStorage.getItem("username") || ""
  );

  function refreshAuthentication() {
    setToken(localStorage.getItem("token") || "");
    setUsername(localStorage.getItem("username") || "");
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken("");
    setUsername("");
  }

  useEffect(() => {
    const handleAuthChange = () => {
      refreshAuthentication();
    };

    window.addEventListener("auth-change", handleAuthChange);

    return () => {
      window.removeEventListener("auth-change", handleAuthChange);
    };
  }, []);

  if (!token) {
    return (
      <div className="app-shell">
        <Auth onAuthSuccess={refreshAuthentication} />
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Navbar username={username} onLogout={handleLogout} />

      <main className="container">
        <AddApplication />

        <Dashboard />
      </main>
    </div>
  );
}

export default App;