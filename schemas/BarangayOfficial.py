from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, constr
from datetime import datetime

from typing import Optional
class BarangayOfficialSchema(BaseModel):
    first_name: constr(min_length=1, max_length=255)
    middle_name: constr(min_length=1, max_length=255)
    last_name: constr(min_length=1, max_length=255)
    suffix: Optional[constr(min_length=1, max_length=255)] = None
    birthday: Optional[constr(min_length=1, max_length=255)] = None
    email: Optional[constr(min_length=1, max_length=255)] = None
    contact_no: Optional[constr(min_length=1, max_length=255)] = None
    position: Optional[constr(min_length=1, max_length=255)] = None
    start_term: Optional[constr(min_length=1, max_length=255)] = None
    end_term:  Optional[constr(min_length=1, max_length=255)] = None
    photo_path: Optional[constr(min_length=1, max_length=255)] = None




