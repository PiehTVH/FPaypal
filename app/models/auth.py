from pydantic import BaseModel

class Token(BaseModel):
    """Response template for the JWT generation endpoint."""
    token: str

class StandardResponseToken(BaseModel):
    code: int
    success: bool
    data: Token