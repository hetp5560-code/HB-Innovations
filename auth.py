from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from werkzeug.security import generate_password_hash, check_password_hash

from config import get_db_connection

import sqlite3
auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = None

        try:
            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO users(full_name,email,password)
                VALUES(?,?,?)
                """,
                (full_name, email, hashed_password)
            )

            conn.commit()

            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:
            flash(
                "This email is already registered. Please use another email or login to your account.",
                "error"
            )
            return redirect(url_for("auth.register"))

        finally:
            if conn:
                conn.close()

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]

            return redirect(url_for("dashboard"))

        flash(
            "The email or password you entered is incorrect. Please check your details and try again.",
            "error"
        )

        return redirect(url_for("auth.login"))

    return render_template("login.html")