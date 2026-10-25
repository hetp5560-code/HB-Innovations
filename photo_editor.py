from flask import Blueprint, render_template, session, redirect

photo_editor = Blueprint("photo_editor", __name__)


@photo_editor.route("/photo-editor")
def photo_editor_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("photo_editor.html")