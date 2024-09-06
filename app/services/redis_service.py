import redis
from app.core.config import settings


redis_client = None


def init_redis() -> None:
    """Initialize Redis Client or return the existing client."""
    global redis_client
    if not redis_client:
        redis_client = redis.Redis.from_url(settings.redis_url)
    return redis_client


def store_paypal_jwt_token(token: str, client_id: str, exp: int = 1000) -> None:
    """Save the PayPal token in Redis."""
    redis_client = init_redis()
    redis_client.set(f"paypal_token:{client_id}", token, ex=exp)
    return None


def get_paypal_jwt_token(client_id: str) -> str:
    """Gets the PayPal token from Redis."""
    redis_client = init_redis()
    token = redis_client.get(f"paypal_token:{client_id}")
    return token.decode("utf-8") if token else None 


def store_paypal_payment_link(payment_id: str, link: str, exp: int = 600000) -> None:
    """Save the PayPal payment link in Redis."""
    redis_client = init_redis()
    redis_client.set(f"paypal_payment_link:{payment_id}", link, ex=exp)
    return None


def get_paypal_payment_link(payment_id: str) -> str:
    """Get the PayPal payment link from Redis."""
    redis_client = init_redis()
    link = redis_client.get(f"paypal_payment_link:{payment_id}")
    return link.decode("utf-8") if link else None