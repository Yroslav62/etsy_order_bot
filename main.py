import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

@app.route("/", methods=["GET"])
def home():
    return "Etsy bot is alive"

@app.route("/etsy", methods=["POST"])
def etsy_webhook():
    data = request.json or {}
    buyer = data.get("buyer", "Unknown")
    total = data.get("total", "N/A")
    order_id = data.get("order_id", "N/A")

    msg = f"🛒 New Etsy Order\n\nOrder ID: {order_id}\nBuyer: {buyer}\nTotal: {total}$"
    send_telegram(msg)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
