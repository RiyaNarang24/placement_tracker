from flask import request, jsonify, g
from database import get_db_connection
from auth import token_required
from flask import g

@token_required

def create_application():
    data = request.get_json()

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO applications (company, role, status, notes, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("company"),
        data.get("role"),
        data.get("status"),
        data.get("notes"),
        g.user_id
    ))

    conn.commit()
    conn.close()

    return {"message": "Application added successfully"}, 201

    return jsonify({"message": "Application added successfully"}), 201
@token_required
def get_user_applications():
    conn = get_db_connection()
    applications = conn.execute(
        "SELECT * FROM applications WHERE user_id = ?",
        (g.user_id,)
    ).fetchall()
    conn.close()

    return jsonify([dict(app) for app in applications])
@token_required
def update_application(id):
    data = request.get_json()

    conn = get_db_connection()
    conn.execute("""
        UPDATE applications
        SET company = COALESCE(?, company),
            role = COALESCE(?, role),
            status = COALESCE(?, status),
            notes = COALESCE(?, notes)
        WHERE id = ? AND user_id = ?
    """, (
        data.get("company"),
        data.get("role"),
        data.get("status"),
        data.get("notes"),
        id,
        g.user_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Application updated successfully"})
@token_required
def delete_application(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM applications WHERE id = ? AND user_id = ?",
        (id, g.user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Application deleted successfully"})