

from  flask_cors import CORS
from applications import (
    create_application,
    get_user_applications,
    update_application,
    delete_application
)
from auth import token_required, register_user, login_user
from database import get_db_connection, init_db
from flask import g
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)
    
init_db()
@app.route("/")
def home():
    return "Server is running!"

@app.route("/applications", methods=["POST"])
def add_application():
    return create_application()


@app.route("/applications", methods=["GET"])
def get_applications():
    return get_user_applications()


@app.route("/applications/<int:id>", methods=["PUT"])
def update_app(id):
    return update_application(id)


@app.route("/applications/<int:id>", methods=["DELETE"])
def delete_app(id):
    return delete_application(id)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status = register_user(data)
    return jsonify(response), status


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status = login_user(data)
    return jsonify(response), status

if __name__ == "__main__":
    app.run()

