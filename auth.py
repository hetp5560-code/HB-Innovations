from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_db_connection

import os
import smtplib
import sqlite3
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint("auth", __name__)

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


def send_welcome_email(full_name, email):
    """Send a welcome email after a new user registers."""
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        raise RuntimeError(
            "Email credentials are missing. Check MAIL_USERNAME and "
            "MAIL_PASSWORD in your .env file."
        )

    message = EmailMessage()
    message["Subject"] = "Welcome to HB Innovations!"
    message["From"] = MAIL_USERNAME
    message["To"] = email

    message.set_content(
        f"""Hi {full_name},

Welcome to HB Innovations!

We are happy to have you as a member of our creative community.

With HB Innovations, you can:
- Create beautiful photo collages.
- Explore creative photo editing tools.
- Design and download amazing memories.
- Build your own creative designs.

Your creativity makes HB Innovations special!

Start exploring and bring your ideas to life.

Your Creativity. Your Memories. Your Style.

Best regards,
Team HB Innovations
"""
    )

    # Try Gmail's standard SSL connection first.
    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()

        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(message)

    print("Welcome email sent successfully!")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        hashed_password = generate_password_hash(password)
        conn = None

        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO users (full_name, email, password)
                VALUES (?, ?, ?)
                """,
                (full_name, email, hashed_password),
            )
            conn.commit()

        except sqlite3.IntegrityError:
            flash(
                "This email is already registered. Please use another email "
                "or log in to your account.",
                "error",
            )
            return redirect(url_for("auth.register"))

        finally:
            if conn:
                conn.close()

        # Registration is saved before attempting to send the welcome email.
        try:
            send_welcome_email(full_name, email)
            flash(
                "Registration successful! A welcome email has been sent "
                "to your email address.",
                "success",
            )
        except Exception as error:
            print("Welcome email error:", repr(error))
            flash(
                "Registration successful, but the welcome email could not "
                "be sent. Please check the email settings.",
                "error",
            )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db_connection()
        try:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,),
            ).fetchone()
        finally:
            conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            return redirect(url_for("dashboard"))

        flash(
            "The email or password you entered is incorrect. "
            "Please check your details and try again.",
            "error",
        )
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
