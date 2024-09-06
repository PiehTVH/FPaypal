from fastapi import APIRouter, Depends, HTTPException
from app.services.redis_service import get_paypal_jwt_token, get_paypal_payment_link, store_paypal_payment_link
from app.services.paypal_service import generate_payment_link
from app.utils.responses import standard_response
from app.core.security import validate_jwt_token
from app.models.payment import PaymentUrlResponse, StandardResponsePayment, PaymentRequest, PaymentResponse
from fastapi.security import OAuth2PasswordBearer
import uuid

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/api/payment/generate", response_model=StandardResponsePayment, tags=["Payments"])
async def generate_payment(payment: PaymentRequest, token: str = Depends(oauth2_scheme)):
    """Generates a PayPal payment link and returns the id."""
    
    payment_id = str(uuid.uuid4())
    
    amount = payment.amount
    expiration = payment.expires_in
    
    payload = validate_jwt_token(token)
    
    client_id = payload["id"]
    
    if not client_id:
        raise Exception("Invalid token")
    
    paypal_token = get_paypal_jwt_token(client_id)
    
    if not paypal_token:
        raise Exception("PayPal Token Not Found")

    payment_link = generate_payment_link(paypal_token, amount)

    store_paypal_payment_link(payment_id, payment_link, expiration)
    
    response = PaymentResponse(id=payment_id)
    
    return standard_response(response.model_dump())


@router.get("/api/payment/{payment_id}", tags=["Payments"])
async def get_payment(payment_id: str, token: str = Depends(oauth2_scheme)):
    """Gets the PayPal payment link and redirects to the link."""
    
    try:
        payload = validate_jwt_token(token)
        client_id = payload.get("id")
        
        if not client_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        payment_link = get_paypal_payment_link(payment_id)

        if not payment_link:
            raise HTTPException(status_code=404, detail="Payment link not found")

        response = PaymentUrlResponse(url=payment_link)

        return standard_response(response.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))