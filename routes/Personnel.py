from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.database import get_db
from models.Personnel import Personnel
from models.User import User
from schemas.Personnel import PersonnelSchema
from schemas.User import UserSchema
from auth.Oauth2 import get_current_user
from datetime import datetime
from pydantic import UUID4
from typing import Optional
import base64
import uuid
import os
from uuid import UUID

router = APIRouter(prefix="/personnels", tags=["Personnels"])

#Get All Personnel Profiles
@router.get("/all")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    personnels = db.query(Personnel).filter(Personnel.deleted_at == None).all()

    data = []

    for personnel in personnels:
        # Convert image to base64
        with open(personnel.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(personnel.id),
            "first_name": personnel.first_name,
            "middle_name": personnel.middle_name,
            "last_name": personnel.last_name,
            "suffix": personnel.suffix,
            "birthday": personnel.birthday,
            "email": personnel.email,
            "contact_no": personnel.contact_no,
            "position": personnel.position,

            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(personnel.created_by),
            "updated_at": personnel.updated_at,
            "updated_by": str(personnel.updated_by),
            "deleted_at": personnel.deleted_at,
            "deleted_by": str(personnel.deleted_by),
        })

    return {
        "message": "Personnels fetched successfully!",
        "data": data
    }

#Get All Deleted Personnel Profiles
@router.get("/deleted")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    personnels = db.query(Personnel).filter(Personnel.deleted_at != None).all()

    data = []

    for personnel in personnels:
        # Convert image to base64
        with open(personnel.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(personnel.id),
            "first_name": personnel.first_name,
            "middle_name": personnel.middle_name,
            "last_name": personnel.last_name,
            "suffix": personnel.suffix,
            "birthday": personnel.birthday,
            "email": personnel.email,
            "contact_no": personnel.contact_no,
            "position": personnel.position,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(personnel.created_by),
            "updated_at": personnel.updated_at,
            "updated_by": str(personnel.updated_by),
            "deleted_at": personnel.deleted_at,
            "deleted_by": str(personnel.deleted_by),
        })

    return {
        "message": "Personnels fetched successfully!",
        "data": data
    }

# Get all PERSONNELS || Pagination
@router.get("/getp")
async def index(
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):

    # Calculate the offset based on the page and limit
    offset = (page - 1) * limit

    # Query Personnels with pagination and search
    query = db.query(Personnel).filter(Personnel.deleted_at == None)

    if search:
        # Use OR condition to search in multiple columns
        query = query.filter(
            or_(
                Personnel.first_name.ilike(f"%{search}%"),
                Personnel.last_name.ilike(f"%{search}%"),
                Personnel.position.ilike(f"%{search}%"),
                # Add more columns as needed
            )
        )

    personnels = query.offset(offset).limit(limit).all()

    data = []

    for personnel in personnels:
        # Convert image to base64
        with open(personnel.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(personnel.id),
            "first_name": personnel.first_name,
            "middle_name": personnel.middle_name,
            "last_name": personnel.last_name,
            "suffix": personnel.suffix,
            "birthday": personnel.birthday,
            "email": personnel.email,
            "contact_no": personnel.contact_no,
            "position": personnel.position,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(personnel.created_by),
            "updated_at": personnel.updated_at,
            "updated_by": str(personnel.updated_by),
            "deleted_at": personnel.deleted_at,
            "deleted_by": str(personnel.deleted_by),
        })

    return {
        "message": "Personnels fetched successfully!",
        "data": data,
        "page": page,
        "limit": limit
    }

# Get Specific Barangay Official
@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    personnel = db.query(Personnel).filter(Personnel.id == id,
                                                          Personnel.deleted_at == None).first()

    if personnel:
        # Convert image to base64
        with open(personnel.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        return {
            "message": f"Barangay official fetched successfully {personnel.id}",
            "data": {
                "id": personnel.id,
                "first_name": personnel.first_name,
                "middle_name": personnel.middle_name,
                "last_name": personnel.last_name,
                "suffix": personnel.suffix,
                "birthday": personnel.birthday,
                "email": personnel.email,
                "contact_no": personnel.contact_no,
                "position": personnel.position,
                "photo_path": encoded_image,  # Include base64-encoded image data
                "created_at": personnel.created_at,
                "created_by": personnel.created_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Personnel does not exist!")

UPLOADS_DIR = "images/Personnels"  # Define your folder directory path here

@router.post("/add")
async def store(
        first_name: str = Form(...),
        middle_name: str = Form(...),
        last_name: str = Form(...),
        suffix: str = Form(...),
        birthday: str = Form(...),
        email: str = Form(...),
        contact_no: str = Form(...),
        position: str = Form(...),
        photo_path: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user.email).first()
    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    try:
        # Save the uploaded image file
        profile_photo_path = save_profile_photo(photo_path, UPLOADS_DIR)

        personnel = Personnel(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            birthday=birthday,
            email=email,
            contact_no=contact_no,
            position=position,
            photo_path=profile_photo_path,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(personnel)
        db.commit()

        data = {
            "first_name": personnel.first_name,
            "middle_name": personnel.middle_name,
            "last_name": personnel.last_name,
            "suffix": personnel.suffix,
            "birthday": personnel.birthday,
            "email": personnel.email,
            "contact_no": personnel.contact_no,
            "position": personnel.position,
            "photo_path": personnel.photo_path,
            "created_at": personnel.created_at,
            "created_by": personnel.created_by
        }

        return {
            "message": "Personnel Successfully Added!",
            "data": data
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
def save_profile_photo(photo_path: UploadFile, upload_dir: str):
    # Generate a unique filename for the uploaded image
    file_extension = photo_path.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"

    # Save the image to the specified directory
    save_path = os.path.join(upload_dir, filename)

    with open(save_path, "wb") as image_file:
        image_file.write(photo_path.file.read())

    return save_path
@router.put("/{id}")
async def update_personnel(id: UUID, request: PersonnelSchema, photo_path: UploadFile = File(None),
                           db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    user = db.query(User).filter(User.email == current_user.email).first()
    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id

    personnel = db.query(Personnel).filter(Personnel.id == id, Personnel.deleted_at == None).first()

    if not personnel:
        raise HTTPException(status_code=404, detail="Personnel does not exist!")

    # Update fields
    personnel.first_name = request.first_name
    personnel.middle_name = request.middle_name
    personnel.last_name = request.last_name
    personnel.suffix = request.suffix
    personnel.birthday = request.birthday
    personnel.email = request.email
    personnel.contact_no = request.contact_no
    personnel.position = request.position
    personnel.updated_at = datetime.now()
    personnel.updated_by = userid

    if photo_path:
        # Save the uploaded image file
        profile_photo_path = save_profile_photo(photo_path, UPLOADS_DIR)
        personnel.photo_path = profile_photo_path

    db.commit()

    return {
        "message": f"Personnel with ID {id} updated successfully",
        "data": {
            "first_name": personnel.first_name,
            "middle_name": personnel.middle_name,
            "last_name": personnel.last_name,
            "suffix": personnel.suffix,
            "birthday": personnel.birthday,
            "email": personnel.email,
            "contact_no": personnel.contact_no,
            "position": personnel.position,
            "created_at": personnel.created_at,
            "created_by": personnel.created_by,
            "updated_at": personnel.updated_at,
            "updated_by": personnel.updated_by
        }
    }

#Delete Personnel
@router.delete("/{id}")
async def delete(id: UUID, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Retrieve the personnel
    personnel = db.query(Personnel).filter(Personnel.id == id,
                                                          Personnel.deleted_at == None).first()

    user = db.query(User).filter(User.email == current_user.email).first()

    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    if personnel:
        # Get the file path from the personnel official data
        file_path = personnel.photo_path

        # Delete the image file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Update personnel data to mark it as deleted
        personnel.deleted_at = datetime.now()
        personnel.deleted_by = userid
        db.commit()

        return {"message": "Personnel deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Personnel does not exist!")