from config.database import Base
from sqlalchemy import Column, String, Text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID

import uuid


class ClearancePermit(Base):
    __tablename__ = "clearances_permit"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_of_resident = Column(String(100), nullable=True)
    type_of_request = Column(String(100), nullable=True)
    request = Column(String(100), nullable=True)
    permit = Column(String(100), nullable=True)
    reason = Column(String(100), nullable=True)
    contact_no = Column(Numeric(precision=10, scale=0), nullable=True)
    email = Column(String(100), nullable=True)
    valid_id_path = Column(String(255), nullable=True)
    date_requested = Column(String(100), nullable=True)
    date_scheduled = Column(String(100), nullable=True)
    date_released = Column(String(100), nullable=True)
    date_received = Column(String(100), nullable=True)

    # Mandatory columns
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

