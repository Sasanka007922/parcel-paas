from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import secrets
from app.core.database import Base

class User(Base):
    __tablename__="users"

    id: Mapped[str] = mapped_column(
        String(32), 
        primary_key=True, 
        default=lambda: f"usr_{secrets.token_hex(12)}"
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    auth_providers: Mapped[list["AuthProvider"]] = relationship(
        "AuthProvider",
        back_populates="user",
        cascade="all,delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )