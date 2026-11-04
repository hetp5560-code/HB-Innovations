from flask import Blueprint, render_template, session, redirect
from tracking import log_activity

photo_editor = Blueprint("photo_editor", __name__)


@photo_editor.route("/photo-editor")
def photo_editor_page():

    if "user_id" not in session:
        return redirect("/login")

    log_activity(session["user_id"], "Opened Photo Editor", "Opened the photo editor page")
    return render_template("photo_editor.html")