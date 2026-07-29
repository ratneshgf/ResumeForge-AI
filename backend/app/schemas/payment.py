from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    session_id: str
    plan: str = "premium_single"


class CreateOrderResponse(BaseModel):
    order_id: str
    amount: int  # in paise
    currency: str = "INR"
    key_id: str
    mock_mode: bool


class VerifyPaymentRequest(BaseModel):
    session_id: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class VerifyPaymentResponse(BaseModel):
    verified: bool
    premium_unlocked: bool
