from pydantic import BaseModel
from typing import Optional


class PaymentBody(BaseModel):
    """Here you could declare objects which send you payment service"""
    event: Optional[str] = None
    object: dict
