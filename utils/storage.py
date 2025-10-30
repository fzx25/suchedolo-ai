import os, json, functools
from flask import session, redirect, url_for, flash

DATA_FILE = os.path.join("data", "database.json")

DEFAULT_DB = {
    "users": [],
    "classes": [],
    "subjects": [],
    "exams": [],
    "homeworks": []
}

def ensure_db():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DB, f, ensure_ascii=False, indent=2)

def load_db():
    ensure_db()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def next_id(seq):
    return (max((item["id"] for item in seq), default=0) + 1)

def get_user(username):
    db = load_db()
    return next((u for u in db["users"] if u["username"] == username), None)

def add_user(username, password):
    db = load_db()
    db["users"].append({"username": username, "password": password})
    save_db(db)

def verify_user(username, password):
    u = get_user(username)
    return bool(u and u["password"] == password)

def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please login first.")
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)
    return wrapper
