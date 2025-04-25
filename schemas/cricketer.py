"""Cricketer Pydantic models"""

from pydantic import BaseModel


class CricketBase(BaseModel):
    """Basic Pydantic model for cricketer"""

    name: str
    age: int
    country: str
    role: str
    team_id: int


class CricketCreate(CricketBase):
    """Pydantic model for creating new cricketer"""


class CricketRead(CricketBase):
    """Pydantic model for reading crickter"""

    id: int

    class Config:
        """Allow creating model from ORM object"""

        from_attributes = True
