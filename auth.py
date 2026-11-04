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


# BREVO SMTP SETTINGS

BREVO_SMTP_LOGIN = os.getenv("BREVO_SMTP_LOGIN")
BREVO_SMTP_KEY = os.getenv("BREVO_SMTP_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")


# SEND WELCOME EMAIL

def send_welcome_email(full_name, email):

    if not BREVO_SMTP_LOGIN or not BREVO_SMTP_KEY or not BREVO_SENDER_EMAIL:
        print("Brevo credentials are missing.")
        return False

    message = EmailMessage()

    message["Subject"] = "Welcome to HB Innovations!"
    message["From"] = f"HB Innovations <{BREVO_SENDER_EMAIL}>"
    message["To"] = email

    message.set_content(
        f"""Hi {full_name},

Welcome to HB Innovations!

We are happy to have you as a member of our creative community.

With HB Innovations, you can:
- Create beautiful photo collages.
- Explore creative photo editing tools.
- Design and download amazing memories.

Your Creativity. Your Memories. Your Style.

Best regards,
Team HB Innovations
"""
    )

    try:

        context = ssl.create_default_context()

        with smtplib.SMTP(
            "smtp-relay.brevo.com",
            587,
            timeout=30
        ) as server:

            server.ehlo()

            server.starttls(context=context)

            server.ehlo()

            server.login(
                BREVO_SMTP_LOGIN,
                BREVO_SMTP_KEY
            )

            server.send_message(message)

        print("Brevo welcome email sent successfully!")

        return True

    except Exception as error:

        print("Brevo email failed:", repr(error))

        return False


# USER REGISTRATION

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
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
                (full_name, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            flash("This email is already registered.", "error")

            return redirect(url_for("auth.register"))

        except Exception as error:

            print("Registration error:", repr(error))

            flash("Registration failed. Please try again.", "error")

            return redirect(url_for("auth.register"))

        finally:

            if conn:
                conn.close()

        # Send Welcome Email using Brevo
        email_sent = send_welcome_email(full_name, email)

        if email_sent:

            flash(
                "Registration successful! Welcome email sent.",
                "success"
            )

        else:

            flash(
                "Registration successful! Welcome email could not be sent.",
                "success"
            )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# USER LOGIN

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db_connection()

        try:

            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

        finally:

            conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]

            return redirect(url_for("dashboard"))

        flash("Incorrect email or password.", "error")

        return redirect(url_for("auth.login"))

    return render_template("login.html")


# USER LOGOUT

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))