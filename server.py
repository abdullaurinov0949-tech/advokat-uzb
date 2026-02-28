import os
import requests
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

# ================= CONFIG =================

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("TOKEN yoki CHAT_ID environment variable topilmadi")

# ================= APP INIT =================

app = Flask(__name__)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)
CORS(app, origins=[
    "https://advokat-frontend.onrender.com"
])

# ================= ROUTES =================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend ishlayapti ✅"}), 200


@app.route("/send", methods=["POST"])
@limiter.limit("3 per minute")
def send():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data required"}), 400
        website = data.get("website")

        if website:
            return jsonify({"error": "Bot detected"}), 400

        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        lawyer = data.get("lawyer", "").strip()
        text = data.get("text", "").strip()

        
        # ========= VALIDATION =========

        if not re.match(r"^\+998\d{9}$", phone):
         return jsonify({"error": "Invalid phone format"}), 400

        if len(name) < 5:
          return jsonify({"error": "Name too short"}), 400

        if len(text) < 5:
          return jsonify({"error": "Message too short"}), 400

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