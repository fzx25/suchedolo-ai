from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

ai_chat_bp = Blueprint("ai_chat", __name__, url_prefix="/ai_chat")

# إنشاء عميل OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@ai_chat_bp.route("/", endpoint="ai_chat")
def chat_page():
    return render_template("ai_chat.html")

@ai_chat_bp.route("/ask", methods=["POST"])
def ask_ai():
    user_message = request.form["message"]
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_reply = response.choices[0].message.content
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})
