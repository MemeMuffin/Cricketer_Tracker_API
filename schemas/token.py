"""JWT token schema and models"""

from pydantic import BaseModel


class Token(BaseModel):
    """Creates token for authorization"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data associated with token for authentication and permissions"""

    username: str | None = None
    role: str | None = None
