from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),
                unique=True,
                primary_key=True,
                index=True,
                nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime,
                        default=datetime.now,
                        onupdate=datetime.now,
                        nullable=False)

    items = relationship('Item', back_populates='user', lazy='subquery')
