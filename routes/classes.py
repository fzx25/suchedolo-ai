from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .auth import load_db, save_db

classes_bp = Blueprint("classes", __name__, url_prefix="/classes")

@classes_bp.route("/", methods=["GET", "POST"])
def classes():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    db = load_db()
    user = next((u for u in db["users"] if u["username"] == session["username"]), None)

    # ✅ If no user found, redirect or show an error
    if user is None:
        flash("⚠️ User not found. Please log in again.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        grade = request.form.get("grade", "").strip()
        if name and grade:
            # Ensure "classes" key exists
            if "classes" not in user:
                user["classes"] = []

            user["classes"].append({"name": name, "grade": grade})
            save_db(db)
            flash("✅ Class added!", "success")
        else:
            flash("⚠️ Fill all fields!", "error")

    # ✅ Use get() to avoid crash if "classes" doesn't exist
    return render_template("classes.html", classes=user.get("classes", []))


@classes_bp.route("/delete/<int:cid>", methods=["POST"])
def delete_class(cid):
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == session["username"]), None)
    if user and 0 <= cid < len(user["classes"]):
        user["classes"].pop(cid)
        save_db(db)
        flash("🗑️ Class deleted!", "success")
    return redirect(url_for("classes.classes"))
