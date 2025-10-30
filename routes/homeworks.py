from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import json, os, datetime

homeworks_bp = Blueprint("homeworks", __name__, url_prefix="/homeworks")
DB_PATH = "data/database.json"

def load_db():
    if not os.path.exists(DB_PATH):
        return {"users": []}
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

@homeworks_bp.route("/", methods=["GET", "POST"])
def homeworks():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    db = load_db()
    user = next((u for u in db["users"] if u["username"] == username), None)

    if not user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        title = request.form.get("title", "").strip()
        due_date = request.form.get("due_date", "").strip()
        notes = request.form.get("notes", "").strip()

        if subject and title and due_date:
            new_hw = {
                "id": len(user["homeworks"]) + 1,
                "subject": subject,
                "title": title,
                "due_date": due_date,
                "notes": notes,
                "completed": False
            }
            user["homeworks"].append(new_hw)
            save_db(db)
            flash("Homework added successfully!", "success")
        else:
            flash("Please fill in all required fields.", "error")

    return render_template("homeworks.html", homeworks=user["homeworks"])

@homeworks_bp.route("/delete/<int:hw_id>")
def delete_homework(hw_id):
    username = session.get("username")
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == username), None)

    if user:
        user["homeworks"] = [h for h in user["homeworks"] if h["id"] != hw_id]
        save_db(db)
        flash("Homework deleted successfully!", "success")

    return redirect(url_for("homeworks.homeworks"))
