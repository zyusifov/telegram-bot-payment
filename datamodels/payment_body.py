from pydantic import BaseModel


class PaymentBody(BaseModel):
    """Here you could declare objects which send you payment service"""
    data: dict
