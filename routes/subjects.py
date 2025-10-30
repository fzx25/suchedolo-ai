from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.auth import load_db, save_db

subjects_bp = Blueprint("subjects", __name__, url_prefix="/subjects")

@subjects_bp.route("/", methods=["GET", "POST"])
def subjects():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == session["username"]), None)

    if request.method == "POST":
        name = request.form.get("name").strip()
        if name:
            user["subjects"].append({"id": len(user["subjects"]) + 1, "name": name})
            save_db(db)
            flash("✅ Subject added!", "success")
        else:
            flash("⚠️ Enter a subject name!", "error")

    return render_template("subjects.html", subjects=user["subjects"])

@subjects_bp.route("/delete/<int:sid>", methods=["POST"])
def delete_subject(sid):
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == session["username"]), None)
    user["subjects"] = [s for s in user["subjects"] if s["id"] != sid]
    save_db(db)
    flash("🗑️ Subject deleted!", "success")
    return redirect(url_for("subjects.subjects"))
