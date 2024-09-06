from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.utils import responses
from app.services.redis_service import store_paypal_jwt_token
from app.services.paypal_service import authenticate_paypal
from app.core.security import create_jwt_token
from app.models.auth import Token, StandardResponseToken


router = APIRouter()
security = HTTPBasic()


@router.get("/api/auth/login",
            response_model=StandardResponseToken,
            summary="Genera Token JWT",
            description="Authenticates the user with PayPal and returns a JWT token.",
            response_description="Token JWT",
            tags=["Authentication"]
            )
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """Authenticates the user with PayPal and returns a JWT token."""
    client_id = credentials.username
    client_secret = credentials.password
    
    # Authenticate with PayPal, get the token and expiration
    paypal_token, paypal_token_exp = authenticate_paypal(client_id, client_secret)
    
    # Save PayPal token in redis
    store_paypal_jwt_token(paypal_token, client_id, paypal_token_exp)
    
    # Generate a JWT token with the client id
    jwt_token = create_jwt_token(client_id)
    
    # Generate response
    response = Token(token=jwt_token)
    
    # Return the JWT token
    return responses.standard_response(response.model_dump())


