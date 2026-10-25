import os

from flask import Blueprint, render_template, request, redirect, session
from werkzeug.utils import secure_filename

from config import get_db_connection

profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["GET", "POST"])
def profile_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        # ---------------- Photo Upload ----------------

        photo = request.files.get("photo")

        photo_name = None

        if photo and photo.filename != "":

            photo_name = secure_filename(photo.filename)

            profile_folder = "static/uploads/profile"

            os.makedirs(profile_folder, exist_ok=True)

            photo.save(
                os.path.join(
                    profile_folder,
                    photo_name
                )
            )

        # ---------------- Form Data ----------------

        phone = request.form["phone"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        country = request.form["country"]
        pincode = request.form["pincode"]
        about = request.form["about"]

        # ---------------- Existing Profile ----------------

        existing_profile = conn.execute(
            "SELECT * FROM profiles WHERE user_id=?",
            (session["user_id"],)
        ).fetchone()

        if existing_profile:

            if photo_name:

                conn.execute("""
                    UPDATE profiles
                    SET
                        photo=?,
                        phone=?,
                        dob=?,
                        gender=?,
                        address=?,
                        city=?,
                        state=?,
                        country=?,
                        pincode=?,
                        about=?
                    WHERE user_id=?
                """, (
                    photo_name,
                    phone,
                    dob,
                    gender,
                    address,
                    city,
                    state,
                    country,
                    pincode,
                    about,
                    session["user_id"]
                ))

            else:

                conn.execute("""
                    UPDATE profiles
                    SET
                        phone=?,
                        dob=?,
                        gender=?,
                        address=?,
                        city=?,
                        state=?,
                        country=?,
                        pincode=?,
                        about=?
                    WHERE user_id=?
                """, (
                    phone,
                    dob,
                    gender,
                    address,
                    city,
                    state,
                    country,
                    pincode,
                    about,
                    session["user_id"]
                ))

        else:

            conn.execute("""
                INSERT INTO profiles
                (
                    user_id,
                    photo,
                    phone,
                    dob,
                    gender,
                    address,
                    city,
                    state,
                    country,
                    pincode,
                    about
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                photo_name,
                phone,
                dob,
                gender,
                address,
                city,
                state,
                country,
                pincode,
                about
            ))

        conn.commit()
        conn.close()

        return redirect("/education")

    # ---------------- Load Data ----------------

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    profile_data = conn.execute(
        "SELECT * FROM profiles WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user,
        profile=profile_data
    )