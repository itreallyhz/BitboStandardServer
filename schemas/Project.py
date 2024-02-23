from typing import Optional
from pydantic import BaseModel, constr
from uuid import UUID
from datetime import datetime


class ProjectSchema(BaseModel):
    title: Optional[constr(min_length=0, max_length=100)] = None
    projType: Optional[constr(min_length=0, max_length=100)] = None
    description: Optional[constr(min_length=0, max_length=100)] = None
    status: Optional[constr(min_length=0, max_length=100)] = None
    duration: Optional[constr(min_length=0, max_length=100)] = None
    started: Optional[constr(min_length=0, max_length=100)] = None
    budget: Optional[constr(min_length=0, max_length=100)] = None
    source: Optional[constr(min_length=0, max_length=100)] = None