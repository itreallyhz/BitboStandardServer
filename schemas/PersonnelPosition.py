from pydantic import BaseModel, constr

class PersonnelPositionSchema(BaseModel):
    position: constr(min_length=1, max_length=100)
    configuration_id: str