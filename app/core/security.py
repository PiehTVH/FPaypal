import jwt
from app.core.config import settings
from fastapi import HTTPException, status, Depends


SECRET_KEY = settings.secret_key


def create_jwt_token(client_id: str) -> str:
    """Create a JWT token with the client id"""
    payload = {"id": client_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validate_jwt_token(token: str):
    """Validates the JWT token and returns the client id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )