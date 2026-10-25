from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

projects = Blueprint("projects", __name__)

@projects.route("/projects", methods=["GET", "POST"])
def projects_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        project_name = request.form["project_name"]
        description = request.form["description"]
        github_link = request.form["github_link"]

        existing = conn.execute(
            "SELECT * FROM projects WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        if existing:

            conn.execute("""
                UPDATE projects
                SET
                    project_name = ?,
                    description = ?,
                    github_link = ?
                WHERE user_id = ?
            """, (
                project_name,
                description,
                github_link,
                session["user_id"]
            ))

        else:

            conn.execute("""
                INSERT INTO projects
                (user_id, project_name, description, github_link)
                VALUES (?, ?, ?, ?)
            """, (
                session["user_id"],
                project_name,
                description,
                github_link
            ))

        conn.commit()
        conn.close()

        return redirect("/certificates")

    project_data = conn.execute(
        "SELECT * FROM projects WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "projects.html",
        project=project_data
    )