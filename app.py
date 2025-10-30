from flask import Flask, render_template, redirect, url_for, session
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from routes.auth import auth_bp
from routes.classes import classes_bp
from routes.subjects import subjects_bp
from routes.exams import exams_bp
from routes.homeworks import homeworks_bp
from routes.ai_timetable import ai_bp
from reminder_checker import check_reminders
from routes.study_plan import study_bp
from flask import session
from utils.translations import translations          # ✅ import dictionary
from routes.lang import lang_bp
from routes.ai_chat import ai_chat_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Email configuration (Gmail example)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'suchdoloappreminder@gmail.com'       # replace with your Gmail
app.config['MAIL_PASSWORD'] = 'fmkuzbifmdanibpo'# use App Password (not your real one)
app.config['MAIL_DEFAULT_SENDER'] = 'suchdoloappreminder@gmail.com'
mail = Mail(app)

# ✅ Register all Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(classes_bp)
app.register_blueprint(subjects_bp)
app.register_blueprint(exams_bp)
app.register_blueprint(homeworks_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(study_bp)
app.register_blueprint(lang_bp)
app.register_blueprint(ai_chat_bp)
# ✅ Add this here — BEFORE any route definitions
@app.context_processor
def inject_translations():
    lang = session.get("lang", "en")
    return dict(t=translations.get(lang), lang=lang)
# ✅ Dashboard route
@app.route("/")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/future-vision")
def future_vision():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("future_vision.html", username=session["username"])

# ✅ Scheduler to check reminders every 24 hours
scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='email_reminder', hours=1)
def scheduled_task():
    with app.app_context():
        check_reminders(mail)
        print("✅ Reminder check completed")


scheduler.start()

# ✅ Run the app
if __name__ == "__main__":
    app.run(debug=True)

