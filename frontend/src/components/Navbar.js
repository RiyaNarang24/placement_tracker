function Navbar({ username, onLogout }) {
  return (
    <header>
      <h1>Job Application Tracker</h1>

      <div className="header-right">
        <span id="welcome-msg">Welcome, {username}!</span>

        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}

export default Navbar;