import hmac
import json
import os
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from config import get_db_connection
from dotenv import load_dotenv

load_dotenv()

admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.admin_login"))
        return view_function(*args, **kwargs)
    return wrapped_view


def _fetch_resume_data(user_id):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT id, full_name, email, created_at FROM users WHERE id=?", (user_id,)).fetchone()
        if not user:
            return None
        profile = conn.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,)).fetchone()
        education = conn.execute("SELECT * FROM education WHERE user_id=?", (user_id,)).fetchone()
        experience = conn.execute("SELECT * FROM experience WHERE user_id=?", (user_id,)).fetchone()
        skills = conn.execute("SELECT * FROM skills WHERE user_id=?", (user_id,)).fetchone()
        projects = conn.execute("SELECT * FROM projects WHERE user_id=?", (user_id,)).fetchone()
        certificates = conn.execute("SELECT * FROM certificates WHERE user_id=? ORDER BY id", (user_id,)).fetchall()
        return {
            "user": dict(user),
            "profile": dict(profile) if profile else {},
            "education": dict(education) if education else {},
            "experience": dict(experience) if experience else {},
            "skills": dict(skills) if skills else {},
            "projects": dict(projects) if projects else {},
            "certificates": [dict(row) for row in certificates]
        }
    finally:
        conn.close()


@admin.route("/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        expected_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
        expected_password = os.getenv("ADMIN_PASSWORD", "")

        if not expected_email or not expected_password:
            flash("Admin credentials are not configured. Add ADMIN_EMAIL and ADMIN_PASSWORD to environment variables.", "error")
            return redirect(url_for("admin.admin_login"))

        email_ok = hmac.compare_digest(email, expected_email)
        password_ok = hmac.compare_digest(password, expected_password)

        if email_ok and password_ok:
            session.clear()
            session["admin_logged_in"] = True
            session["admin_email"] = expected_email
            return redirect(url_for("admin.admin_dashboard"))

        flash("Incorrect admin email or password.", "error")

    return render_template("admin_login.html")


@admin.route("/logout")
@admin_required
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_email", None)
    return redirect(url_for("admin.admin_login"))


@admin.route("/")
@admin.route("/dashboard")
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    try:
        total_users = conn.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
        total_resumes = conn.execute("SELECT COUNT(*) AS total FROM resume_history").fetchone()["total"]
        today_users = conn.execute("SELECT COUNT(*) AS total FROM users WHERE date(created_at)=date('now')").fetchone()["total"]
        active_today = conn.execute("SELECT COUNT(DISTINCT user_id) AS total FROM activity_logs WHERE date(created_at)=date('now')").fetchone()["total"]
        recent_activities = conn.execute("""
            SELECT activity_logs.*, users.full_name, users.email
            FROM activity_logs LEFT JOIN users ON users.id=activity_logs.user_id
            ORDER BY activity_logs.id DESC LIMIT 12
        """).fetchall()
        recent_users = conn.execute("SELECT id, full_name, email, created_at FROM users ORDER BY id DESC LIMIT 6").fetchall()
    finally:
        conn.close()
    return render_template(
        "admin_dashboard.html", total_users=total_users, total_resumes=total_resumes,
        today_users=today_users, active_today=active_today,
        recent_activities=recent_activities, recent_users=recent_users
    )


@admin.route("/users")
@admin_required
def admin_users():
    search = request.args.get("q", "").strip()
    conn = get_db_connection()
    try:
        if search:
            users = conn.execute("""
                SELECT u.id, u.full_name, u.email, u.created_at,
                       (SELECT COUNT(*) FROM resume_history r WHERE r.user_id=u.id) AS resume_count
                FROM users u WHERE u.full_name LIKE ? OR u.email LIKE ?
                ORDER BY u.id DESC
            """, (f"%{search}%", f"%{search}%")).fetchall()
        else:
            users = conn.execute("""
                SELECT u.id, u.full_name, u.email, u.created_at,
                       (SELECT COUNT(*) FROM resume_history r WHERE r.user_id=u.id) AS resume_count
                FROM users u ORDER BY u.id DESC
            """).fetchall()
    finally:
        conn.close()
    return render_template("admin_users.html", users=users, search=search)


@admin.route("/users/<int:user_id>")
@admin_required
def admin_user_detail(user_id):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT id, full_name, email, created_at FROM users WHERE id=?", (user_id,)).fetchone()
        if not user:
            abort(404)
        profile = conn.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,)).fetchone()
        education = conn.execute("SELECT * FROM education WHERE user_id=?", (user_id,)).fetchone()
        experience = conn.execute("SELECT * FROM experience WHERE user_id=?", (user_id,)).fetchone()
        skills = conn.execute("SELECT * FROM skills WHERE user_id=?", (user_id,)).fetchone()
        projects = conn.execute("SELECT * FROM projects WHERE user_id=?", (user_id,)).fetchone()
        certificates = conn.execute("SELECT * FROM certificates WHERE user_id=? ORDER BY id DESC", (user_id,)).fetchall()
        resumes = conn.execute("SELECT id, template_name, action, created_at FROM resume_history WHERE user_id=? ORDER BY id DESC", (user_id,)).fetchall()
        activities = conn.execute("SELECT * FROM activity_logs WHERE user_id=? ORDER BY id DESC LIMIT 30", (user_id,)).fetchall()
    finally:
        conn.close()
    return render_template(
        "admin_user_detail.html", user=user, profile=profile, education=education,
        experience=experience, skills=skills, projects=projects,
        certificates=certificates, resumes=resumes, activities=activities
    )


@admin.route("/activities")
@admin_required
def admin_activities():
    conn = get_db_connection()
    try:
        activities = conn.execute("""
            SELECT activity_logs.*, users.full_name, users.email
            FROM activity_logs LEFT JOIN users ON users.id=activity_logs.user_id
            ORDER BY activity_logs.id DESC LIMIT 250
        """).fetchall()
    finally:
        conn.close()
    return render_template("admin_activities.html", activities=activities)


@admin.route("/resumes/<int:resume_id>")
@admin_required
def admin_resume_preview(resume_id):
    conn = get_db_connection()
    try:
        record = conn.execute("""
            SELECT r.*, u.full_name, u.email
            FROM resume_history r JOIN users u ON u.id=r.user_id
            WHERE r.id=?
        """, (resume_id,)).fetchone()
    finally:
        conn.close()
    if not record:
        abort(404)
    data = json.loads(record["snapshot_json"] or "{}")
    template_name = str(record["template_name"])
    if template_name == "modern":
        return render_template("resume_modern.html", **data, admin_preview=True, admin_resume_id=resume_id)
    if not template_name.isdigit() or not (1 <= int(template_name) <= 25):
        abort(404)
    return render_template("resume_template.html", template=template_name, **data, admin_preview=True, admin_resume_id=resume_id)
