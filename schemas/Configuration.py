from pydantic import BaseModel, constr
from typing import Optional

class ConfigurationSchema(BaseModel):
    region: constr(min_length=1, max_length=100)
    province: Optional[constr(min_length=0, max_length=100)] = None
    municipality: Optional[constr(min_length=0, max_length=100)] = None
    district: constr(min_length=1, max_length=100)
    barangay: constr(min_length=1, max_length=100)





