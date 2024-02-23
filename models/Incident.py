from sqlalchemy.orm import relationship

from config.database import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_title = Column(String(255), nullable=True)
    case_description = Column(String(255), nullable=True)
    complainant = Column(String(255), nullable=True)
    witness = Column(String(255), nullable=True)
    officer = Column(String(255), nullable=True)
    subject_complaint = Column(String(255), nullable=True)
    place = Column(String(255), nullable=True)
    happened = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    photo_path = Column(String(255), nullable=True)
    # resident_id = Column(UUID(as_uuid=True), ForeignKey("residentprofiles.id"), nullable=False)

    # Mandatory columns
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    # Relationship
    # barangay_official_ordinance = relationship("Ordinance", back_populates="ordinance_barangay_official")
