from pydantic import BaseModel, constr
from fastapi import UploadFile

class OrdinanceSchema(BaseModel):


    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)
    description: str
    file: UploadFile

    ##barangay_official_id: str