import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from applications import (
    create_application,
    delete_application,
    get_user_applications,
    update_application,
)
from auth import login_user, register_user
from database import init_db


BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_ROOT = os.path.abspath(
    os.path.join(BACKEND_DIR, "..", "frontend")
)
FRONTEND_BUILD = os.path.join(FRONTEND_ROOT, "build")

if os.path.isfile(os.path.join(FRONTEND_BUILD, "index.html")):
    FRONTEND_DIR = FRONTEND_BUILD
else:
    FRONTEND_DIR = FRONTEND_ROOT


app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000,http://localhost:5173",
    ).split(",")
    if origin.strip()
]

CORS(app, origins=allowed_origins)

init_db()


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "placement-tracker",
    })


@app.route("/<path:path>", methods=["GET"])
def static_files(path):
    requested_file = os.path.join(FRONTEND_DIR, path)

    if os.path.isfile(requested_file):
        return send_from_directory(FRONTEND_DIR, path)

    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/applications", methods=["POST"])
def add_application():
    return create_application()


@app.route("/applications", methods=["GET"])
def get_applications():
    return get_user_applications()


@app.route("/applications/<int:application_id>", methods=["PUT"])
def update_app(application_id):
    return update_application(application_id)


@app.route("/applications/<int:application_id>", methods=["DELETE"])
def delete_app(application_id):
    return delete_application(application_id)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    response, status = register_user(data)
    return jsonify(response), status


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    response, status = login_user(data)
    return jsonify(response), status


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )