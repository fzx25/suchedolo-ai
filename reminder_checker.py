from datetime import datetime
import json
from flask_mail import Message

def send_reminder_email(to, subject_name, due_date, type_, mail):
    msg = Message(
        subject=f"Reminder: {type_} coming up soon!",
        recipients=[to],
        body=f"Don’t forget! Your {type_} for {subject_name} is due on {due_date}. Good luck!"
    )
    mail.send(msg)
    print(f"✅ Email sent to {to} for {type_}: {subject_name} (due {due_date})")

def check_reminders(mail):
    with open("data/database.json", "r") as f:
        db = json.load(f)

    now = datetime.now()
    print("🕒 Checking reminders at", now.strftime("%Y-%m-%d %H:%M"))

    for user in db["users"]:
        email = user.get("email")
        if not email:
            print("⚠️ No email for user:", user.get("username"))
            continue

        for hw in user.get("homeworks", []):
            if "due_date" in hw:
                due = datetime.strptime(hw["due_date"], "%Y-%m-%d")
                days_left = (due - now).days
                if 0 <= days_left <= 1:
                    print(f"📘 Found homework due soon: {hw['title']} (in {days_left} days)")
                    send_reminder_email(email, hw["title"], hw["due_date"], "homework", mail)

        for exam in user.get("exams", []):
            if "date" in exam:
                due = datetime.strptime(exam["date"], "%Y-%m-%d")
                days_left = (due - now).days
                if 0 <= days_left <= 1:
                    print(f"📗 Found exam due soon: {exam['subject']} (in {days_left} days)")
                    send_reminder_email(email, exam["subject"], exam["date"], "exam", mail)
