from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import json, os, hashlib

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
DB_PATH = "data/database.json"

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"users": []}, f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    db = load_db()
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        email = request.form.get("email").strip()
        if not username or not password:
            flash("Please fill all fields!", "error")
            return redirect(url_for("auth.register"))
        if any(u["username"] == username for u in db["users"]):
            flash("Username already exists!", "error")
            return redirect(url_for("auth.register"))

        db["users"].append({
            "username": username,
            "password": hash_password(password),
            "email": email,
            "classes": [],
            "subjects": [],
            "exams": [],
            "homeworks": []
        })
        save_db(db)
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    db = load_db()
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = hash_password(request.form.get("password").strip())
        user = next((u for u in db["users"] if u["username"] == username and u["password"] == password), None)
        if user:
            session["username"] = username
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))
