# Placement Tracker

A full-stack web application that helps users track and manage their job applications in one place.

## Features

- User registration and login
- JWT-based authentication
- Add, edit, and delete job applications
- Track application status
- Search applications by company or role
- Filter applications by status
- Sort applications
- Dashboard statistics
- Multi-user support
- Responsive user interface

## Tech Stack

### Frontend

- React.js
- JavaScript
- HTML
- CSS
- Create React App

### Backend

- Python
- Flask
- Flask-CORS
- PyJWT
- python-dotenv
- Gunicorn

### Database

- SQLite

## Architecture

Frontend (React) → REST APIs (Flask) → SQLite Database

The application follows a client-server architecture. The React frontend communicates with Flask REST APIs, while the backend handles authentication, business logic, and database operations.

## Project Structure

    placement_tracker/
    ├── backend/
    │   ├── applications.py
    │   ├── auth.py
    │   ├── database.py
    │   ├── main.py
    │   ├── requirements.txt
    │   └── .env.example
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   │   ├── components/
    │   │   │   ├── AddApplications.js
    │   │   │   ├── Auth.js
    │   │   │   ├── Dashboard.js
    │   │   │   ├── Login.js
    │   │   │   ├── Navbar.js
    │   │   │   └── Register.js
    │   │   ├── App.js
    │   │   ├── App.css
    │   │   ├── index.js
    │   │   └── index.css
    │   ├── package.json
    │   └── package-lock.json
    ├── .gitignore
    └── README.md

## Running Locally

### Backend Setup

Install the backend dependencies:

    pip install -r backend/requirements.txt

Create a file named `backend/.env` and add:

    JWT_SECRET_KEY=replace-with-a-long-random-secret

Start the backend:

    python backend/main.py

The backend runs at:

    http://127.0.0.1:5000

### Frontend Setup

Open another terminal and run:

    cd frontend
    npm install
    npm start

The frontend runs at:

    http://localhost:3000

The React development server forwards API requests to the Flask backend through the proxy configured in `frontend/package.json`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Log in and receive a JWT token |
| GET | `/applications` | Get the logged-in user's applications |
| POST | `/applications` | Create a new application |
| PUT | `/applications/<id>` | Update an application |
| DELETE | `/applications/<id>` | Delete an application |
| GET | `/health` | Check backend status |

## Authentication

JWT authentication is used to protect application routes. After login, the frontend sends the JWT token with protected API requests.

Users can access only their own job applications.

## Security

- Passwords are stored as hashes.
- Protected routes require JWT authentication.
- Users can access only their own applications.
- Secret keys are stored in environment variables.
- `.env` files are excluded from Git.
- Database files are excluded from Git.
- SQL queries use parameters.

## Database Choice

SQLite was selected because this is a lightweight project that is easy to run locally without requiring a separate database server.

For a larger production system, the database can be migrated to PostgreSQL.

## Deployment

The application is deployed on Replit and can be accessed through its existing public URL.

The backend can also be started with Gunicorn:

    gunicorn --bind 0.0.0.0:5000 --reuse-port --chdir backend main:app

## Author

Riya Narang