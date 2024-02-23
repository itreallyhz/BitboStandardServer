from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.User import User
from schemas.User import UserSchema
from schemas.UpdateUser import UpdateUserSchema
from datetime import datetime
from pydantic import UUID4
from hash.Hashing import Hash
import re
#from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["User Account (Secretary)"])

#Secretary

#Get all users
@router.get("/")
async def index(db: Session = Depends(get_db)):

    users = db.query(User).filter(User.deleted_at == None).all()
    data = []
    if users:
        for users in users:
            data.append({
                "id": users.id,
                "first_name": users.first_name,
                "last_name": users.last_name,
                "email": users.email,
                "password": users.password,
            })
        return {
            "message": "All users successfully fetched!",
            "data": data
       }
    else:
        raise HTTPException(status_code=404, detail=f"Users data does not exists!")

#Get a specific user
@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id, User.deleted_at == None).first()

    if user:
        return {
            "message": f"Configuration:{user.id} successfully fetched!",
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password": user.password,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Data does not exists!")

#Update a User with editing password
@router.put("/{id}")
async def update(id: UUID4, request: UpdateUserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id, User.deleted_at == None).first()

    if user:
        user.first_name = request.first_name
        user.last_name = request.last_name
        db.commit()

        return {
            "message": f"First: {user.id} updated successfully",
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
    else:
         raise HTTPException(status_code=404, detail=f"User does not exists!")


#Delete a User
@router.delete("/{id}")
async def delete(id: UUID4, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id, User.deleted_at == None).first()

    if user:
        user.deleted_at = datetime.now()
        user.deleted_by = "f03619a1-08eb-42ed-8152-a48033a5e731"
        db.commit()
        return{"message": "User successfully deleted!"}

    else:
        raise HTTPException(status_code=404, detail=f"Data does not exists.")



#pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/")
async def store(request: UserSchema, db: Session = Depends(get_db)):
    # Password validation regex pattern
    password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:<>?~=\\[\];\',./])(?=.*[0-9a-z]).{8,}$')

    # Check if password meets requirements
    if not password_pattern.match(request.password):
        raise HTTPException(status_code=400, detail="Password does not meet requirements. It should have 8 or more characters, at least 1 uppercase letter, and at least 1 special symbol.")

    user = db.query(User).filter(User.email == request.email).all()

    if user:
        raise HTTPException(status_code=400, detail="User already exists!")

    try:
        user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            password=Hash.bcrypt(request.password),
            user_type="Secretary"
        )
        db.add(user)
        db.commit()
        return {
                "message": "User added successfully!",
                "data": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email":user.email,
                    "password": user.password,
                    "user_type": "Secretary"
                }
            }
    except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

