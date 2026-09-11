import datetime
import os
import sqlite3
from functools import wraps

import jwt
from flask import g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from database import get_db_connection

load_dotenv(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".env",
    )
)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")


def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "").strip()

        if not auth_header:
            return jsonify(
                {"error": "Authorization token is required"}
            ), 401

        token = auth_header

        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()

        try:
            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"],
            )
            g.user_id = decoded["user_id"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authorization token"}), 401

        return function(*args, **kwargs)

    return decorated


def register_user(data):
    if not isinstance(data, dict):
        return {"error": "Request body must be valid JSON."}, 400

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return {"error": "Username and password are required."}, 400

    if len(username) < 3:
        return {"error": "Username must contain at least 3 characters."}, 400

    if len(username) > 50:
        return {"error": "Username must be 50 characters or fewer."}, 400

    if len(password) < 6:
        return {"error": "Password must contain at least 6 characters."}, 400

    if len(password) > 128:
        return {"error": "Password must be 128 characters or fewer."}, 400

    hashed_password = generate_password_hash(password)
    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, hashed_password),
        )
        connection.commit()

    except sqlite3.IntegrityError:
        return {"error": "Username already exists."}, 409

    finally:
        connection.close()

    return {"message": "User registered successfully."}, 201


def login_user(data):
    if not isinstance(data, dict):
        return {"error": "Request body must be valid JSON."}, 400

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return {"error": "Username and password are required."}, 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            """
            SELECT id, username, password
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    finally:
        connection.close()

    if user is None or not check_password_hash(
        user["password"],
        password,
    ):
        return {"error": "Invalid username or password."}, 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return {
        "message": "Login successful.",
        "token": token,
        "username": user["username"],
    }, 200