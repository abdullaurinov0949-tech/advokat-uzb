import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# ================= CONFIG =================

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("TOKEN yoki CHAT_ID environment variable topilmadi")

# ================= APP INIT =================

app = Flask(__name__)

CORS(app, origins=[
    "https://advokat-uzb-1.onrender.com"
])

# ================= ROUTES =================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend ishlayapti ✅"}), 200


@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data required"}), 400

        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        lawyer = data.get("lawyer", "").strip()
        text = data.get("text", "").strip()

        # ========= VALIDATION =========

        if not all([name, phone, lawyer, text]):
            return jsonify({"error": "All fields required"}), 400

        if len(text) > 1000:
            return jsonify({"error": "Message too long"}), 400

        if not phone.startswith("+998") or len(phone) != 13:
            return jsonify({"error": "Invalid phone format"}), 400

        # ========= TELEGRAM MESSAGE =========

        message = f"""
📩 Yangi murojaat
👤 Ism: {name}
📞 Telefon: {phone}
⚖️ Advokat: {lawyer}
📝 Muammo:
{text}
"""

        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        response = requests.post(
            telegram_url,
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({"error": "Telegram API error"}), 502

        return jsonify({"status": "ok"}), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Telegram timeout"}), 504

    except Exception as e:
        print("Server error:", e)
        return jsonify({"error": "Internal server error"}), 500


# ================= MAIN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)