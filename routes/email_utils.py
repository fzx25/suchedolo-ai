from flask_mail import Message
from app import mail

def send_reminder_email(to, subject_name, due_date, type_):
    msg = Message(
        subject=f"Reminder: {type_} coming up soon!",
        recipients=[to],
        body=f"Don’t forget! Your {type_} for {subject_name} is due on {due_date}. Good luck! 🧠"
    )
    mail.send(msg)
