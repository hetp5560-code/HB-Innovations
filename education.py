from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

education = Blueprint("education", __name__)

@education.route("/education", methods=["GET", "POST"])
def education_page():

    # Login Check
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    # =======================
    # SAVE / UPDATE EDUCATION
    # =======================
    if request.method == "POST":

        degree = request.form["degree"]
        institute = request.form["institute"]
        passing_year = request.form["passing_year"]
        cgpa = request.form["cgpa"]

        existing = conn.execute(
            "SELECT * FROM education WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if existing:

            conn.execute("""
                UPDATE education
                SET
                    degree = ?,
                    institute = ?,
                    passing_year = ?,
                    cgpa = ?
                WHERE user_id = ?
            """, (
                degree,
                institute,
                passing_year,
                cgpa,
                session["user_id"]
            ))

        else:

            conn.execute("""
                INSERT INTO education
                (user_id, degree, institute, passing_year, cgpa)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                degree,
                institute,
                passing_year,
                cgpa
            ))

        conn.commit()
        conn.close()

        return redirect("/experience")

    # =======================
    # LOAD EDUCATION DATA
    # =======================

    education_data = conn.execute(
        "SELECT * FROM education WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "education.html",
        education=education_data
    )