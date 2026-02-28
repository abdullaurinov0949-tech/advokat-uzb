from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/send", methods=["POST"])
def send():
    data = request.json


    name = data.get("name")
    phone = data.get("phone")
    lawyer = data.get("lawyer")
    text = data.get("text")

    message = f"""📩 Yangi murojaat
👤 {name}
📞 {phone}
⚖️ {lawyer}
📝 {text}"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    