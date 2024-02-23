from sqlalchemy.orm import relationship



from config.database import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid


class Personnel(Base):
    __tablename__ = "personnels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    suffix = Column(String(255), nullable=True)
    birthday = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    contact_no = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    photo_path = Column(String(255), nullable=True)
    #resident_id = Column(UUID(as_uuid=True), ForeignKey("residentprofiles.id"), nullable=False)


    # Mandatory tables
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

#Relationship
#personnel_resident = relationship("ResidentProfile", back_populates="resident_personnel")
#personnel_personnelposition = relationship("PersonnelPosition", back_populates="personnelposition_personnel")