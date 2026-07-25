from datetime import datetime
import enum
from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import secrets
from app.core.database import Base

class ProviderType(str, enum.Enum):
    EMAIL="email"
    GITHUB="github"
    GOOGLE="google"

class AuthProvider(Base):

    __tablename__ = "auth_providers"

    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user_id"),
    )

    id: Mapped[str] = mapped_column(
        String(32), 
        primary_key=True, 
        default=lambda: f"atp_{secrets.token_hex(12)}"
    )

    user_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    provider: Mapped[ProviderType] = mapped_column(
        Enum(ProviderType),
        nullable=False
    )

    provider_user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user: Mapped["User"] = relationship(
        "User", 
        back_populates="auth_providers"
    )
