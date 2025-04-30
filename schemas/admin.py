"""Schemas for administrator"""

from pydantic import BaseModel


class AdministratorBase(BaseModel):
    """Base pydantic model for administrator"""

    name: str
    username: str
    password: str
    is_superuser: bool | None = False


class CreateAdministrator(AdministratorBase):
    """Administrator pydantic model for creation"""


class UpdateAdministrator(BaseModel):
    """Administrator pydantic model for updation"""

    name: str | None = None
    username: str | None = None
    password: str | None = None
    is_superuser: bool | None = None


class ReadAdministrator(AdministratorBase):
    """Administrator pydantic model for reading"""

    id: int

    class Config:
        """Allow reading ORM objects"""

        from_attributes = True
