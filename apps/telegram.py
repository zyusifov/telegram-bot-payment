import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_TOKEN")


def send_message(chat_id, text):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "MarkdownV2"
    }
    r = requests.post(
        url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
    return r


def send_payment_button(chat_id, text, payment_link):
    data = {
        "chat_id": chat_id,
        "text": f"{text}",
        "parse_mode": "MarkdownV2",
        "reply_markup": json.dumps({
                "inline_keyboard": [[{
                    "text": "Pay now!",
                    "url": f"{payment_link}"
                }]]
        })
    }
    r = requests.post(
        url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
    return r
