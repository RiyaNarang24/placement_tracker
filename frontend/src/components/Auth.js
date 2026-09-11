import { useState } from "react";
import Login from "./Login";
import Register from "./Register";

function Auth({ onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [registrationMessage, setRegistrationMessage] = useState("");

  function handleRegistrationSuccess() {
    setIsLogin(true);
    setRegistrationMessage("Registration successful. You can now log in.");
  }

  function handleLoginSuccess() {
    setRegistrationMessage("");
    onAuthSuccess();
  }

  return (
    <div id="auth-screen" className="screen auth-screen">
      <div className="auth-card">
        <h1>Job Tracker</h1>

        <div className="tab-buttons">
          <button
            className={`tab-btn ${isLogin ? "active" : ""}`}
            onClick={() => {
              setIsLogin(true);
              setRegistrationMessage("");
            }}
          >
            Login
          </button>

          <button
            className={`tab-btn ${!isLogin ? "active" : ""}`}
            onClick={() => {
              setIsLogin(false);
              setRegistrationMessage("");
            }}
          >
            Register
          </button>
        </div>

        {isLogin ? (
          <Login onAuthSuccess={handleLoginSuccess} />
        ) : (
          <Register onAuthSuccess={handleRegistrationSuccess} />
        )}

        <div className="success-msg">{registrationMessage}</div>
      </div>
    </div>
  );
}

export default Auth;