import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

certificates = Blueprint("certificates", __name__)


@certificates.route("/certificates", methods=["GET", "POST"])
def certificates_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        certificate_name = request.form["certificate_name"]
        organization = request.form["organization"]
        year = request.form["year"]

        certificate = request.files.get("certificate_file")
        certificate_file = ""

        if certificate and certificate.filename != "":

            certificate_file = secure_filename(certificate.filename)

            upload_folder = "static/uploads/certificates"

            os.makedirs(upload_folder, exist_ok=True)

            certificate.save(
                os.path.join(upload_folder, certificate_file)
            )

        conn.execute("""
            INSERT INTO certificates
            (
                user_id,
                certificate_name,
                organization,
                year,
                certificate_file
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            certificate_name,
            organization,
            year,
            certificate_file
        ))

        conn.commit()
        conn.close()

        return redirect("/templates")

    certificates_data = conn.execute(
        "SELECT * FROM certificates WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "certificates.html",
        certificates=certificates_data
    )