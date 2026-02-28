from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app, origins=["https://advokat-uzb-1.onrender.com"])

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)
@app.route("/")
def home():
    return "Backend ishlayapti ✅"

@app.route("/send", methods=["POST"])
def send():
    data = request.json

    name = data.get("name")
    phone = data.get("phone")
    lawyer = data.get("lawyer")
    text = data.get("text")

    if not name or not phone or not lawyer or not text:
        return jsonify({"error": "Invalid data"}), 400

    if len(text) > 1000:
        return jsonify({"error": "Message too long"}), 400

    message = f"""
📩 Yangi murojaat
👤 {name}
📞 {phone}
⚖️ {lawyer}
📝 {text}"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    if response.status_code != 200:
        return jsonify({"error": "Telegram failed"}), 500

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)