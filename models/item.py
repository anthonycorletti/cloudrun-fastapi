from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True),
                unique=True,
                primary_key=True,
                index=True,
                nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime,
                        default=datetime.now,
                        onupdate=datetime.now,
                        nullable=False)
    deleted_at = Column(DateTime, nullable=True)
