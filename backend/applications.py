from flask import g, jsonify, request

from auth import token_required
from database import get_db_connection


VALID_STATUSES = {"Applied", "Interview", "Offer", "Rejected"}


def validate_application(data):
    if not isinstance(data, dict):
        return None, "Request body must be valid JSON."

    company = str(data.get("company", "")).strip()
    role = str(data.get("role", "")).strip()
    status = str(data.get("status", "Applied")).strip()
    notes = str(data.get("notes", "")).strip()

    if not company:
        return None, "Company is required."

    if not role:
        return None, "Role is required."

    if len(company) > 100:
        return None, "Company name must be 100 characters or fewer."

    if len(role) > 100:
        return None, "Role must be 100 characters or fewer."

    if len(notes) > 500:
        return None, "Notes must be 500 characters or fewer."

    if status not in VALID_STATUSES:
        return None, "Invalid application status."

    return {
        "company": company,
        "role": role,
        "status": status,
        "notes": notes,
    }, None


@token_required
def create_application():
    data = request.get_json(silent=True) or {}
    application, error = validate_application(data)

    if error:
        return jsonify({"error": error}), 400

    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO applications
            (company, role, status, notes, user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                application["company"],
                application["role"],
                application["status"],
                application["notes"],
                g.user_id,
            ),
        )
        connection.commit()

    finally:
        connection.close()

    return jsonify(
        {"message": "Application added successfully"}
    ), 201


@token_required
def get_user_applications():
    connection = get_db_connection()

    try:
        applications = connection.execute(
            """
            SELECT id, company, role, status, notes
            FROM applications
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (g.user_id,),
        ).fetchall()

    finally:
        connection.close()

    return jsonify([dict(application) for application in applications])


@token_required
def update_application(application_id):
    data = request.get_json(silent=True) or {}
    application, error = validate_application(data)

    if error:
        return jsonify({"error": error}), 400

    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE applications
            SET company = ?, role = ?, status = ?, notes = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                application["company"],
                application["role"],
                application["status"],
                application["notes"],
                application_id,
                g.user_id,
            ),
        )
        connection.commit()

    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Application not found"}), 404

    return jsonify(
        {"message": "Application updated successfully"}
    )


@token_required
def delete_application(application_id):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM applications
            WHERE id = ? AND user_id = ?
            """,
            (application_id, g.user_id),
        )
        connection.commit()

    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Application not found"}), 404

    return jsonify(
        {"message": "Application deleted successfully"}
    )