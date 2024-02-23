from typing import Optional
from pydantic import BaseModel, constr
from uuid import UUID
from datetime import datetime


class ResidentProfileSchema(BaseModel):
    first_name: Optional[constr(min_length=0, max_length=255)] = None
    middle_name: Optional[constr(min_length=0, max_length=255)] = None
    last_name: Optional[constr(min_length=0, max_length=255)] = None
    suffix: Optional[constr(min_length=0, max_length=255)] = None
    age: Optional[constr(min_length=0, max_length=255)] = None
    birthday: Optional[constr(min_length=0, max_length=255)] = None
    birth_order: Optional[constr(min_length=0, max_length=255)] = None
    birth_place: Optional[constr(min_length=0, max_length=255)] = None
    blood_type: Optional[constr(min_length=0, max_length=255)] = None
    sex: Optional[constr(min_length=0, max_length=255)] = None
    civil_status: Optional[constr(min_length=0, max_length=255)] = None
    house_no: Optional[constr(min_length=0, max_length=255)] = None
    street: Optional[constr(min_length=0, max_length=255)] = None
    phone_no: Optional[constr(min_length=0, max_length=255)] = None
    email: Optional[constr(min_length=0, max_length=255)] = None
    occupation: Optional[constr(min_length=0, max_length=255)] = None
    # For Employed
    educational_attainment: Optional[constr(min_length=0, max_length=255)] = None
    emp_school: Optional[constr(min_length=0, max_length=255)] = None
    emp_degree: Optional[constr(min_length=0, max_length=255)] = None
    emp_company: Optional[constr(min_length=0, max_length=255)] = None
    emp_position: Optional[constr(min_length=0, max_length=255)] = None
    emp_salary: Optional[constr(min_length=0, max_length=255)] = None
    years_employed: Optional[constr(min_length=0, max_length=255)] = None
    #For Occupation:Students
    educational_level: Optional[constr(min_length=0, max_length=255)] = None
    #For Occupation:Students:Elem
    elem_grade_level: Optional[constr(min_length=0, max_length=255)] = None
    #For Occupation:Students:Highschool
    hs_grade_level: Optional[constr(min_length=0, max_length=255)] = None
    #For Occupation:Students:SHS
    shs_grade_level: Optional[constr(min_length=0, max_length=255)] = None
    shs_strand: Optional[constr(min_length=0, max_length=255)] = None
    # For Occupation:Students:College
    college_course: Optional[constr(min_length=0, max_length=255)] = None
    college_year: Optional[constr(min_length=0, max_length=255)] = None
    college_school: Optional[constr(min_length=0, max_length=255)] = None

    ethnicity: Optional[constr(min_length=0, max_length=255)] = None
    religion: Optional[constr(min_length=0, max_length=255)] = None

    is_indigenous: Optional[constr(min_length=0, max_length=255)] = None
    indigenous_type: Optional[constr(min_length=0, max_length=255)] = None

    is_pwd: Optional[constr(min_length=0, max_length=255)] = None
    pwd_id: Optional[constr(min_length=0, max_length=255)] = None

    is_single_parent: Optional[constr(min_length=0, max_length=255)] = None

    is_registered_voter: Optional[constr(min_length=0, max_length=255)] = None
    voting_precint_no: Optional[constr(min_length=0, max_length=255)] = None

    SSS_no: Optional[constr(min_length=0, max_length=255)] = None
    GSIS_no: Optional[constr(min_length=0, max_length=255)] = None
    TIN_no: Optional[constr(min_length=0, max_length=255)] = None

    valid_id: Optional[constr(min_length=0, max_length=255)] = None

    # Mother's Information
    m_first_name: Optional[constr(min_length=0, max_length=255)] = None
    m_middle_name: Optional[constr(min_length=0, max_length=255)] = None
    m_last_name: Optional[constr(min_length=0, max_length=255)] = None
    m_blk: Optional[constr(min_length=0, max_length=255)] = None
    m_street: Optional[constr(min_length=0, max_length=255)] = None
    m_birthday: Optional[constr(min_length=0, max_length=255)] = None
    m_sex: Optional[constr(min_length=0, max_length=255)] = None
    m_phone_no: Optional[constr(min_length=0, max_length=255)] = None
    m_email: Optional[constr(min_length=0, max_length=255)] = None

    # Father's Information
    f_first_name: Optional[constr(min_length=0, max_length=255)] = None
    f_middle_name: Optional[constr(min_length=0, max_length=255)] = None
    f_last_name: Optional[constr(min_length=0, max_length=255)] = None
    f_suffix: Optional[constr(min_length=0, max_length=255)] = None
    f_blk: Optional[constr(min_length=0, max_length=255)] = None
    f_street: Optional[constr(min_length=0, max_length=255)] = None
    f_birthday: Optional[constr(min_length=0, max_length=255)] = None
    f_sex: Optional[constr(min_length=0, max_length=255)] = None
    f_phone_no: Optional[constr(min_length=0, max_length=255)] = None
    f_email: Optional[constr(min_length=0, max_length=255)] = None


