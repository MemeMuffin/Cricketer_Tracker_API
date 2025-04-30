"""Schemas for superusers"""

from pydantic import BaseModel


class SuperuserBase(BaseModel):
    """Base pydantic model for superuser"""

    name: str
    username: str
    password: str
    admin_id: int | None = None


class CreateSuperuser(SuperuserBase):
    """Creation pydantic model for superuser"""


class UpdateSuperuser(BaseModel):
    """Updatation pydantic model for superuser"""

    name: str | None = None
    username: str | None = None
    password: str | None = None
    admin_id: int | None = None


class ReadSuperuser(SuperuserBase):
    """Reading pydantic model for superuser"""

    id: int

    class Config:
        """Allows reading of ORM objects"""

        from_attributes = True
