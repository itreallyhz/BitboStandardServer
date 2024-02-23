from pydantic import BaseModel, constr

class UpdateUserSchema(BaseModel):
    first_name: constr(min_length=3, max_length=50)
    last_name: constr(min_length=3, max_length=50)


