"""Models for superuser"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.admin import Administrator


class Superuser(SQLModel, table=True):
    """Model for superuser"""

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    username: str = Field(index=True)
    password: str = Field(index=True)
    admin_id: int | None = Field(foreign_key="administrator.id", default=None, unique=True)

    # Relationship with administrator
    admin: Optional["Administrator"] = Relationship(back_populates="superuser")
