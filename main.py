from apps import payment, telegram
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from datamodels.telegram_body import TelegramBody
from datamodels.payment_body import PaymentBody
import uvicorn


app = FastAPI()


# Telegram send requests to this url
@app.post("/")
def main(obj: TelegramBody):
    obj = obj.message
    chat_id = obj["chat"]["id"]
    user = obj["from"]["first_name"]
    try:
        payment_link = payment.create_invoice(chat_id)
    except:
        payment_link = "https://google.az/"
    text = f"Hello, *{user}*\\!"

    r = telegram.send_payment_button(chat_id, text, payment_link)
    return {'ok': True}


# Payment service redirect user to this url
@app.get("/success/", response_class=PlainTextResponse)
def success():
    return "Payment was successful"


# Payment service send requests to this url
@app.post("/confirm_payment/")
def confirm_payment(response: PaymentBody):
    """status, success, meta, chat_id - all this params must be declared in payment service"""
    obj = response.object
    chat_id = obj["metadata"]["chat_id"]

    if response.event == "payment.succeeded":
        text = "Payment was successful"
        telegram.send_message(chat_id, text)
    else:
        text = "Payment was failed"
        telegram.send_message(chat_id, text)
    return {'ok': True}


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8001,
        debug=False,
        reload=True,
    )
