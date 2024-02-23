from pydantic import BaseModel, constr
from typing import Optional
from fastapi import UploadFile
class ClearancePermitSchema(BaseModel):
    type_of_request:  Optional[constr(min_length=1, max_length=10)] = None
    name_of_resident: constr(min_length=1, max_length=100)
    request: constr(min_length=1, max_length=100)
    permit: constr(min_length=1, max_length=100)
    reason: Optional[constr(min_length=1, max_length=10)] = None
    contact_no: Optional[constr(min_length=1, max_length=100)] = None
    email: Optional[constr(min_length=1, max_length=100)] = None
    valid_id: UploadFile
    date_requested: Optional[constr(min_length=1, max_length=100)] = None
    date_scheduled: Optional[constr(min_length=1, max_length=100)] = None
    date_released:  Optional[constr(min_length=1, max_length=100)] = None
    date_received: Optional[constr(min_length=1, max_length=100)] = None






