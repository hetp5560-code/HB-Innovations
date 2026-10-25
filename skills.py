from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

skills = Blueprint("skills", __name__)

@skills.route("/skills", methods=["GET", "POST"])
def skills_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        skill_name = request.form["skill_name"]

        existing = conn.execute(
            "SELECT * FROM skills WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if existing:

            conn.execute("""
                UPDATE skills
                SET skill_name = ?
                WHERE user_id = ?
            """, (
                skill_name,
                session["user_id"]
            ))

        else:

            conn.execute("""
                INSERT INTO skills
                (user_id, skill_name)
                VALUES (?, ?)
            """, (
                session["user_id"],
                skill_name
            ))

        conn.commit()
        conn.close()

        return redirect("/projects")

    skills_data = conn.execute(
        "SELECT * FROM skills WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "skills.html",
        skills=skills_data
    )