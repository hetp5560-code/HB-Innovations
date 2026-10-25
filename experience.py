from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

experience = Blueprint("experience", __name__)

@experience.route("/experience", methods=["GET", "POST"])
def experience_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        duration = request.form["duration"]
        description = request.form["description"]

        existing = conn.execute(
            "SELECT * FROM experience WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if existing:

            conn.execute("""
                UPDATE experience
                SET
                    company = ?,
                    role = ?,
                    duration = ?,
                    description = ?
                WHERE user_id = ?
            """, (
                company,
                role,
                duration,
                description,
                session["user_id"]
            ))

        else:

            conn.execute("""
                INSERT INTO experience
                (user_id, company, role, duration, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                company,
                role,
                duration,
                description
            ))

        conn.commit()
        conn.close()

        return redirect("/skills")

    experience_data = conn.execute(
        "SELECT * FROM experience WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "experience.html",
        experience=experience_data
    )