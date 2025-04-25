"""Team Pydantic models"""

from pydantic import BaseModel


class TeamBase(BaseModel):
    """Basic Pydantic model for team"""

    name: str
    country: str


class TeamCreate(TeamBase):
    """Pydantic model for creating new team"""


class TeamRead(TeamBase):
    """Pydantic model for reading team"""

    id: int

    class Config:
        """Allow creating model from ORM object"""

        from_attributes = True
