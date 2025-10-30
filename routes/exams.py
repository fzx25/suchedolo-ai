from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.auth import load_db, save_db

exams_bp = Blueprint("exams", __name__, url_prefix="/exams")

@exams_bp.route("/", methods=["GET", "POST"])
def exams():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == session["username"]), None)

    if request.method == "POST":
        subject = request.form.get("subject").strip()
        date = request.form.get("date").strip()
        if subject and date:
            user["exams"].append({"id": len(user["exams"]) + 1, "subject": subject, "date": date})
            save_db(db)
            flash("✅ Exam added!", "success")
        else:
            flash("⚠️ Fill all fields!", "error")

    return render_template("exams.html", exams=user["exams"])

@exams_bp.route("/delete/<int:eid>", methods=["POST"])
def delete_exam(eid):
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == session["username"]), None)
    user["exams"] = [e for e in user["exams"] if e["id"] != eid]
    save_db(db)
    flash("🗑️ Exam deleted!", "success")
    return redirect(url_for("exams.exams"))
