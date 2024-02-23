from config.database import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    projType = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)
    duration = Column(String(100), nullable=False)
    started = Column(String(100), nullable=False)
    budget = Column(String(100), nullable=False)
    source = Column(String(100), nullable=False)

    # Mandatory columns
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

