import json
import requests
from typing import Tuple
from app.core.config import settings


PAYPAL_URL = settings.paypal_url


def authenticate_paypal(client_id: str, client_secret: str) -> Tuple[str, int]:
    """Authenticate with PayPal and return the access token"""
    
    PAYPAL_LOGIN_API = f"{PAYPAL_URL}/v1/oauth2/token"
    PAYPAL_HEADERS = {"Accept": "application/json", "Accept-Language": "en_US"}
    PAYPAL_DATA = {'grant_type': 'client_credentials'}
    PAYPAL_AUTH = (client_id, client_secret)
    
    auth_response = requests.post(PAYPAL_LOGIN_API, 
                                  headers=PAYPAL_HEADERS, 
                                  data=PAYPAL_DATA,
                                  auth=PAYPAL_AUTH)
    
    if auth_response.status_code == 200:
        auth_response_json = auth_response.json()
        
        token = auth_response_json["access_token"]
        exp = auth_response_json["expires_in"]
        
        if not token:
            raise Exception("Failed to get PayPal token")
        
        return token, exp
    else:
        raise Exception(f"Failed to authenticate with PayPal")

    
def generate_payment_link(access_token: str, value: float = 10.00) -> str:
    """Generates a PayPal payment link and returns the link."""
    PAYPAL_API = f"{PAYPAL_URL}/v1/payments/payment"

    PAYPAL_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    PAYPAL_DATA = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(value),
                "currency": "USD",
            },
            "description": "Pay",
        }],
        "redirect_urls": {
            'return_url': 'http://example.com/return',
            'cancel_url': 'http://example.com/cancel',
        },
    }
    
    payment_response = requests.post(PAYPAL_API, headers=PAYPAL_HEADERS, data=json.dumps(PAYPAL_DATA))
    
    if payment_response.status_code != 201:
        raise Exception("Failed to generate PayPal payment link")
    
    payment_response_json = payment_response.json()
    
    approval_url = None

    for link in payment_response_json['links']:
        if link["rel"] == "approval_url":
            approval_url = link["href"]
            break
        
    return approval_url