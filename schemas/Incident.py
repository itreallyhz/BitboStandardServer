from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, constr
from datetime import datetime

from typing import Optional
class IncidentSchema(BaseModel):
    case_title: constr(min_length=1, max_length=255)
    case_description: constr(min_length=1, max_length=255)
    complainant: constr(min_length=1, max_length=255)
    witness: Optional[constr(min_length=1, max_length=255)] = None
    officer: Optional[constr(min_length=1, max_length=255)] = None
    subject_complaint: Optional[constr(min_length=1, max_length=255)] = None
    place: Optional[constr(min_length=1, max_length=255)] = None
    happened: Optional[constr(min_length=1, max_length=255)] = None
    status: Optional[constr(min_length=1, max_length=255)] = None
    photo_path: UploadFile




