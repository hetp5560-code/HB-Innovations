from flask import Blueprint, render_template, session, redirect
from config import get_db_connection

resume = Blueprint("resume", __name__)


@resume.route("/resume")
def resume_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    profile = conn.execute(
        "SELECT * FROM profiles WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    education = conn.execute(
        "SELECT * FROM education WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    experience = conn.execute(
        "SELECT * FROM experience WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    skills = conn.execute(
        "SELECT * FROM skills WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    projects = conn.execute(
        "SELECT * FROM projects WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    certificates = conn.execute(
        "SELECT * FROM certificates WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "resume_modern.html",
        user=user,
        profile=profile,
        education=education,
        experience=experience,
        skills=skills,
        projects=projects,
        certificates=certificates
    )


# ==========================================
# TEMPLATE SELECTION
# ==========================================

@resume.route("/resume/template/<template>")
def resume_template(template):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    profile = conn.execute(
        "SELECT * FROM profiles WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    education = conn.execute(
        "SELECT * FROM education WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    experience = conn.execute(
        "SELECT * FROM experience WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    skills = conn.execute(
        "SELECT * FROM skills WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    projects = conn.execute(
        "SELECT * FROM projects WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    certificates = conn.execute(
        "SELECT * FROM certificates WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "resume_template.html",
        template=template,
        user=user,
        profile=profile,
        education=education,
        experience=experience,
        skills=skills,
        projects=projects,
        certificates=certificates
    )