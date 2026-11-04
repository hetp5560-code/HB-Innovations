from flask import Blueprint, render_template, session, redirect
from config import get_db_connection
from tracking import log_activity, save_resume_history

resume = Blueprint("resume", __name__)


def get_resume_data(user_id):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT id, full_name, email, created_at FROM users WHERE id=?", (user_id,)).fetchone()
        profile_data = conn.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,)).fetchone()
        education_data = conn.execute("SELECT * FROM education WHERE user_id=?", (user_id,)).fetchone()
        experience_data = conn.execute("SELECT * FROM experience WHERE user_id=?", (user_id,)).fetchone()
        skills_data = conn.execute("SELECT * FROM skills WHERE user_id=?", (user_id,)).fetchone()
        projects_data = conn.execute("SELECT * FROM projects WHERE user_id=?", (user_id,)).fetchone()
        certificates_data = conn.execute("SELECT * FROM certificates WHERE user_id=? ORDER BY id", (user_id,)).fetchall()
        return {
            "user": dict(user) if user else {},
            "profile": dict(profile_data) if profile_data else {},
            "education": dict(education_data) if education_data else {},
            "experience": dict(experience_data) if experience_data else {},
            "skills": dict(skills_data) if skills_data else {},
            "projects": dict(projects_data) if projects_data else {},
            "certificates": [dict(row) for row in certificates_data]
        }
    finally:
        conn.close()


@resume.route("/resume")
def resume_page():
    if "user_id" not in session:
        return redirect("/login")

    data = get_resume_data(session["user_id"])
    save_resume_history(session["user_id"], "modern", "Viewed modern resume", data)
    log_activity(session["user_id"], "Resume Preview", "Viewed the modern resume preview")
    return render_template("resume_modern.html", **data)


@resume.route("/resume/template/<template>")
def resume_template(template):
    if "user_id" not in session:
        return redirect("/login")

    if not template.isdigit() or not (1 <= int(template) <= 25):
        return redirect("/templates")

    data = get_resume_data(session["user_id"])
    save_resume_history(session["user_id"], template, "Selected resume template", data)
    log_activity(session["user_id"], "Resume Template Selected", f"Selected resume template {template}")
    return render_template("resume_template.html", template=template, **data)
