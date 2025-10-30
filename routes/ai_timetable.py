from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import json, os, random

ai_bp = Blueprint("ai", __name__)
DB_PATH = "data/database.json"

def load_db():
    if not os.path.exists(DB_PATH):
        return {"users": []}
    with open(DB_PATH, "r") as f:
        return json.load(f)

@ai_bp.route("/generate_timetable", methods=["GET", "POST"])
def generate_timetable():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    db = load_db()
    user = next((u for u in db["users"] if u["username"] == username), None)
    if not user:
        return redirect(url_for("dashboard"))

    timetable = {}
    role = None

    if request.method == "POST":
        role = request.form.get("role")  # student or teacher
        hours_per_day = 8
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # If student, get subjects; if teacher, get classes
        if role == "student":
            data_list = [s["name"] if isinstance(s, dict) else s for s in user.get("subjects", [])]
        else:
            data_list = [c["name"] if isinstance(c, dict) else c for c in user.get("classes", [])]

        # ✅ Check BEFORE generating
        if len(data_list) < 3:
            flash("⚠️ You must add at least 3 subjects before generating a timetable.", "error")
            return render_template("timetable.html", timetable=None, role=role)

        if role == "teacher":
            # Get free period preference
            min_free = int(request.form.get("min_free", 1))
            max_free = int(request.form.get("max_free", 4))

        # ✅ Generate timetable
        for day in days:
            if role == "teacher":
                num_free = random.randint(min_free, max_free)
                num_classes = hours_per_day - num_free
                class_slots = random.sample(data_list, min(num_classes, len(data_list)))
                day_slots = class_slots + ["Free"] * num_free
                random.shuffle(day_slots)
            else:
                # prevent oversampling error
                safe_slots = min(hours_per_day, len(data_list) * 2)
                day_slots = random.sample(data_list * 2, safe_slots)
                while len(day_slots) < hours_per_day:
                    day_slots.append(random.choice(data_list))

            timetable[day] = day_slots[:hours_per_day]

    return render_template("timetable.html", timetable=timetable, role=role)
