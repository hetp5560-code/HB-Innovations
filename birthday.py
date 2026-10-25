from flask import Blueprint, render_template, session, redirect, request

birthday = Blueprint("birthday", __name__)


# =========================
# Birthday Main Page
# =========================
@birthday.route("/birthday")
def birthday_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("birthday.html")


# =========================
# Girl Birthday Templates
# =========================
@birthday.route("/birthday/girl")
def birthday_girl():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "birthday_templates.html",
        category="girl"
    )


# =========================
# Boy Birthday Templates
# =========================
@birthday.route("/birthday/boy")
def birthday_boy():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "birthday_templates.html",
        category="boy"
    )


# =========================
# Birthday Editor
# =========================
@birthday.route("/birthday/editor")
def birthday_editor():

    if "user_id" not in session:
        return redirect("/login")

    # Selected category
    category = request.args.get("category", "girl")

    # Selected template number
    template = request.args.get("template", "1")

    return render_template(
        "birthday_editor.html",
        category=category,
        template=template
    )