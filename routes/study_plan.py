from flask import Blueprint, render_template, request, session
import json, os, random
from datetime import datetime, timedelta

study_bp = Blueprint("study", __name__)
DB_PATH = "data/database.json"

def load_db():
    if not os.path.exists(DB_PATH):
        return {"users": []}
    with open(DB_PATH, "r") as f:
        return json.load(f)

@study_bp.route("/study_plan", methods=["GET", "POST"])
def study_plan():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    db = load_db()
    user = next((u for u in db["users"] if u["username"] == username), None)
    subjects = user.get("subjects", [])

    study_schedule = None

    if request.method == "POST":
        hours_per_day = int(request.form.get("hours"))
        subjects_per_day = int(request.form.get("subjects_per_day"))
        exam_days = 7  # you can change this or make it user-selected

        # Pick random subjects for each day
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        study_schedule = []

        for i in range(exam_days):
            selected_subjects = random.sample(subjects, min(subjects_per_day, len(subjects)))
            study_schedule.append({
                "day": days[i % len(days)],
                "subjects": selected_subjects,
                "hours_each": round(hours_per_day / subjects_per_day, 1)
            })

    return render_template("study_plan.html", study_schedule=study_schedule, subjects=subjects)
