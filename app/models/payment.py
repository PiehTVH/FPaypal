from pydantic import BaseModel

class PaymentResponse(BaseModel):
    """Response template for the payment generation endpoint."""
    id: str

class PaymentRequest(BaseModel):
    """Request template for the payment generation endpoint."""
    amount: float
    expires_in: int

class StandardResponsePayment(BaseModel):
    code: int
    success: bool
    data: PaymentResponse

class PaymentUrlResponse(BaseModel):
    url: str

class StandardResponsePaymentUrl(BaseModel):
    code: int
    success: bool
    data: PaymentUrlResponse