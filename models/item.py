from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base
from models.user import User  # noqa


class Item(Base):
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True),
                unique=True,
                primary_key=True,
                index=True,
                nullable=False)

    user_id = Column(UUID(as_uuid=True),
                     ForeignKey("users.id", ondelete='CASCADE'),
                     nullable=False,
                     index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime,
                        default=datetime.now,
                        onupdate=datetime.now,
                        nullable=False)

    user = relationship('User', back_populates='items', lazy='subquery')
