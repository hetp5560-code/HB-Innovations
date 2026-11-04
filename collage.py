from flask import Blueprint, render_template, session, redirect
from tracking import log_activity

collage = Blueprint("collage", __name__)


@collage.route("/collage")
def collage_page():
    # Keep the Collage Maker available only to logged-in users, like the dashboard.
    if "user_id" not in session:
        return redirect("/login")
    log_activity(session["user_id"], "Opened Collage Maker", "Opened the collage maker page")
    return render_template("collage.html")
