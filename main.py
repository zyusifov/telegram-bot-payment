from apps import payment, telegram
from fastapi import Request, FastAPI
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
    payment_link = payment.get_payment_link(obj)
    text = f"Hello, *{user}*\\!"

    r = telegram.send_payment_button(chat_id, text, payment_link)
    return {'ok': True}


# Payment service redirect user to this url
@app.get("/success/", response_class=PlainTextResponse)
def success():
    return "Payment was successful"


# Payment service send requests to this url
@app.post("/confirm_payment/")
def confirm_payment(obj: PaymentBody):
    """status, success, meta, chat_id - all this params must be declared in payment service"""
    obj = obj.data
    chat_id = obj["meta"]["chat_id"]
    if obj['status'] == 'success':
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
