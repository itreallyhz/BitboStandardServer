from pydantic import BaseModel, constr, EmailStr

class UserSchema(BaseModel):
    first_name: constr(min_length=3, max_length=50)
    last_name: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=3, max_length=50)



