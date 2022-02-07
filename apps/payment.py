import os
import json
from dotenv import load_dotenv
from yookassa import Configuration, Payment

load_dotenv()


def create_invoice(chat_id):
    Configuration.account_id = os.getenv("SHOP_ID")
    Configuration.secret_key = os.getenv("PAYMENT_TOKEN")

    payment = Payment.create({
        "amount": {
            "value": "5",
            "currency": "USD"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.az"
        },
        "capture": True,
        "description": "Ödəniş №1",
        "metadata": {"chat_id": chat_id}
    })

    return payment.confirmation.confirmation_url
