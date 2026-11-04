from flask import Flask, render_template, session, redirect
import sqlite3
import os

from auth import auth
from profile import profile
from education import education
from experience import experience
from skills import skills
from projects import projects
from certificates import certificates
from resume import resume
from photo_editor import photo_editor
from birthday import birthday
from collage import collage
from admin import admin
from tracking import init_tracking_tables, log_activity

from functools import wraps


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads/certificates"
app.secret_key = "hbinnovations_secret_key"

# Database
DATABASE = os.path.join(app.root_path, "database.db")


def init_database():

    if not os.path.exists(DATABASE):

        with sqlite3.connect(DATABASE) as conn:

            schema_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "database",
                "schema.sql"
            )

            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())

    # Unique email index
    with sqlite3.connect(DATABASE) as conn:

        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_users_email_unique
            ON users(email COLLATE NOCASE)
        """)

        conn.commit()


# Initialize Database
init_database()
init_tracking_tables()


# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(education)
app.register_blueprint(experience)
app.register_blueprint(skills)
app.register_blueprint(projects)
app.register_blueprint(certificates)
app.register_blueprint(resume)
app.register_blueprint(photo_editor)
app.register_blueprint(birthday)
app.register_blueprint(collage)
app.register_blueprint(admin)


def login_required(view_function):

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/login")

        return view_function(*args, **kwargs)

    return wrapped_view


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    log_activity(session["user_id"], "Opened Dashboard", "Opened the user dashboard")
    return render_template("dashboard.html")


# Template Selection Page
@app.route("/templates")
def templates_page():

    if "user_id" not in session:
        return redirect("/login")

    log_activity(session["user_id"], "Viewed Resume Templates", "Opened the resume template gallery")
    return render_template("templates.html")


if __name__ == "__main__":
    app.run(debug=True)