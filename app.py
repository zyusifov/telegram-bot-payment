from flask import Flask, request
from apps import payment, telegram

app = Flask(__name__)


# Telegram send requests to this url
@app.route('/', methods=['POST'])
def main():
    obj = request.json

    chat_id = obj["message"]["chat"]["id"]
    user = obj["message"]["from"]["first_name"]
    payment_link = payment.get_payment_link(obj)
    text = f"Hello, *{user}*\\!"

    telegram.send_payment_button(chat_id, text, payment_link)
    return {'ok': True}


# Payment service redirect user to this url
@app.route('/success/')
def success():
    return "Payment was successful"


# Payment service send requests to this url
@app.route('/confirm_payment/', methods=['POST'])
def confirm_payment():
    """status, success, meta, chat_id - all this params must be declared in payment service"""
    obj = request.json
    chat_id = obj["meta"]["chat_id"]
    if obj['status']['success']:
        text = "Payment was successful"

        telegram.send_message(chat_id, text)
    else:
        text = "Payment was failed"

        telegram.send_message(chat_id, text)
    return {'ok': True}
