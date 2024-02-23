from sqlalchemy.orm import relationship

from config.database import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

class Ordinance(Base):
    __tablename__ = "ordinances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text)
    file = Column(String(100), nullable=True)
    #barangay_official_id = Column(UUID(as_uuid=True), ForeignKey("barangayofficials.id"), nullable=False)

    # Mandatory columns
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    #Relationship
    #ordinance_barangay_official = relationship("BarangayOfficial", back_populates="barangay_official_ordinance")