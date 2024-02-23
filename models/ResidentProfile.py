from sqlalchemy.orm import relationship


from config.database import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

class ResidentProfile(Base):
    __tablename__ = "residentprofiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=True)
    first_name = Column(String(255), nullable=True)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    suffix = Column(String(255), nullable=True)
    age = Column(String(255), nullable=True)
    birthday = Column(String(255), nullable=True)
    birth_order = Column(String(255), nullable=True)
    birth_place = Column(String(255), nullable=True)
    blood_type = Column(String(255), nullable=True)
    sex = Column(String(255), nullable=True)
    civil_status = Column(String(255), nullable=True)
    house_no = Column(String(255), nullable=True)
    street = Column(String(255), nullable=True)
    phone_no = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    occupation = Column(String(255), nullable=True)

    # For Employed
    educational_attainment = Column(String(255), nullable=True)
    emp_school = Column(String(255), nullable=True)
    emp_degree = Column(String(255), nullable=True)
    emp_company = Column(String(255), nullable=True)
    emp_position = Column(String(255), nullable=True)
    emp_salary = Column(String(255), nullable=True)
    years_employed = Column(String(255), nullable=True)
    # For Occupation:Students
    educational_level = Column(String(255), nullable=True)
    # For Occupation:Students:Elem
    elem_grade_level = Column(String(255), nullable=True)
    # For Occupation:Students:Highschool
    hs_grade_level = Column(String(255), nullable=True)
    # For Students:Senior Highschool
    shs_grade_level = Column(String(255), nullable=True)
    shs_strand = Column(String(255), nullable=True)
    # For Occupation:Students:College
    college_course = Column(String(255), nullable=True)
    college_year = Column(String(255), nullable=True)
    college_school = Column(String(255), nullable=True)

    ethnicity = Column(String(255), nullable=True)
    religion = Column(String(255), nullable=True)

    is_indigenous = Column(String(255), nullable=True)
    indigenous_type = Column(String(255), nullable=True)

    is_pwd = Column(String(255), nullable=True)
    pwd_id = Column(String(255), nullable=True)

    is_single_parent = Column(String(255), nullable=True)

    # For Voters
    is_registered_voter = Column(String(255), nullable=True)
    voting_precint_no = Column(String(255), nullable=True)

    SSS_no = Column(String(255), nullable=True)
    GSIS_no = Column(String(255), nullable=True)
    TIN_no = Column(String(255), nullable=True)

    valid_id = Column(String(255), nullable=True)

    # Mother's Information
    m_first_name = Column(String(255), nullable=True)
    m_middle_name = Column(String(255), nullable=True)
    m_last_name = Column(String(255), nullable=True)
    m_blk = Column(String(255), nullable=True)
    m_street = Column(String(255), nullable=True)
    m_birthday = Column(String(255), nullable=True)
    m_sex = Column(String(255), nullable=True)
    m_phone_no = Column(String(255), nullable=True)
    m_email = Column(String(255), nullable=True)

    # Father's Information
    f_first_name = Column(String(255), nullable=True)
    f_middle_name = Column(String(255), nullable=True)
    f_last_name = Column(String(255), nullable=True)
    f_suffix = Column(String(255), nullable=True)
    f_blk = Column(String(255), nullable=True)
    f_street = Column(String(255), nullable=True)
    f_birthday = Column(String(255), nullable=True)
    f_sex = Column(String(255), nullable=True)
    f_phone_no = Column(String(255), nullable=True)
    f_email = Column(String(255), nullable=True)

    # Mandatory tables
    created_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

#Relationship
#pinaka unang relationship
#resident_household = relationship("HouseholdProfile", back_populates="household_resident")
#resident_personnel = relationship("Personnel", back_populates="personnel_resident")
