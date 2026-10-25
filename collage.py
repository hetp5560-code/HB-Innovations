from flask import Blueprint, render_template, session, redirect

collage = Blueprint("collage", __name__)


@collage.route("/collage")
def collage_page():
    # Keep the Collage Maker available only to logged-in users, like the dashboard.
    if "user_id" not in session:
        return redirect("/login")
    return render_template("collage.html")
