from typing import Optional
from uuid import UUID
import uuid
import os
import base64
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.database import get_db
from models.BarangayOfficial import BarangayOfficial
from models.User import User
from schemas.BarangayOfficial import BarangayOfficialSchema
from schemas.User import UserSchema
from auth.Oauth2 import get_current_user
from datetime import datetime
from pydantic import UUID4

router = APIRouter(prefix="/barangayofficials", tags=["Barangay Officials"])


# Get All Barangay Officials
@router.get("/all")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    barangay_officials = db.query(BarangayOfficial).filter(BarangayOfficial.deleted_at == None).all()

    data = []

    for barangay_official in barangay_officials:
        # Convert image to base64
        with open(barangay_official.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(barangay_official.id),
            "first_name": barangay_official.first_name,
            "middle_name": barangay_official.middle_name,
            "last_name": barangay_official.last_name,
            "suffix": barangay_official.suffix,
            "birthday": barangay_official.birthday,
            "email": barangay_official.email,
            "contact_no": barangay_official.contact_no,
            "position": barangay_official.position,
            "start_term": barangay_official.start_term,
            "end_term": barangay_official.end_term,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(barangay_official.created_by),
            "updated_at": barangay_official.updated_at,
            "updated_by": str(barangay_official.updated_by),
            "deleted_at": barangay_official.deleted_at,
            "deleted_by": str(barangay_official.deleted_by),
        })

    return {
        "message": "Barangay Officials fetched successfully!",
        "data": data
    }

# Get all Barangay Officials || Pagination
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

    # Query barangay officials with pagination and search
    query = db.query(BarangayOfficial).filter(BarangayOfficial.deleted_at == None)

    if search:
        # Use OR condition to search in multiple columns
        query = query.filter(
            or_(
                BarangayOfficial.first_name.ilike(f"%{search}%"),
                BarangayOfficial.last_name.ilike(f"%{search}%"),
                BarangayOfficial.position.ilike(f"%{search}%"),
                # Add more columns as needed
            )
        )

    barangay_officials = query.offset(offset).limit(limit).all()

    data = []

    for barangay_official in barangay_officials:
        # Convert image to base64
        with open(barangay_official.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(barangay_official.id),
            "first_name": barangay_official.first_name,
            "middle_name": barangay_official.middle_name,
            "last_name": barangay_official.last_name,
            "suffix": barangay_official.suffix,
            "birthday": barangay_official.birthday,
            "email": barangay_official.email,
            "contact_no": barangay_official.contact_no,
            "position": barangay_official.position,
            "start_term": barangay_official.start_term,
            "end_term": barangay_official.end_term,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(barangay_official.created_by),
            "updated_at": barangay_official.updated_at,
            "updated_by": str(barangay_official.updated_by),
            "deleted_at": barangay_official.deleted_at,
            "deleted_by": str(barangay_official.deleted_by),
        })

    return {
        "message": "Barangay Officials fetched successfully!",
        "data": data,
        "page": page,
        "limit": limit
    }

# Get All Deleted Barangay Officials
@router.get("/deleted")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    barangay_officials = db.query(BarangayOfficial).filter(BarangayOfficial.deleted_at != None).all()

    data = []

    for barangay_official in barangay_officials:
        # Convert image to base64
        with open(barangay_official.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(barangay_official.id),
            "first_name": barangay_official.first_name,
            "middle_name": barangay_official.middle_name,
            "last_name": barangay_official.last_name,
            "suffix": barangay_official.suffix,
            "birthday": barangay_official.birthday,
            "email": barangay_official.email,
            "contact_no": barangay_official.contact_no,
            "position": barangay_official.position,
            "start_term": barangay_official.start_term,
            "end_term": barangay_official.end_term,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(barangay_official.created_by),
            "updated_at": barangay_official.updated_at,
            "updated_by": str(barangay_official.updated_by),
            "deleted_at": barangay_official.deleted_at,
            "deleted_by": str(barangay_official.deleted_by),
        })

    return {
        "message": "Barangay Officials fetched successfully!",
        "data": data
    }

# Get All Barangay Officials with Position "Barangay Captain"
@router.get("/barangaycaptain")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    barangay_officials = db.query(BarangayOfficial).filter(
        BarangayOfficial.deleted_at == None,
        BarangayOfficial.position == "Barangay Captain"
    ).all()

    data = []

    for barangay_official in barangay_officials:
        # Convert image to base64
        with open(barangay_official.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(barangay_official.id),
            "first_name": barangay_official.first_name,
            "middle_name": barangay_official.middle_name,
            "last_name": barangay_official.last_name,
            "suffix": barangay_official.suffix,
            "birthday": barangay_official.birthday,
            "email": barangay_official.email,
            "contact_no": barangay_official.contact_no,
            "position": barangay_official.position,
            "start_term": barangay_official.start_term,
            "end_term": barangay_official.end_term,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(barangay_official.created_by),
            "updated_at": barangay_official.updated_at,
            "updated_by": str(barangay_official.updated_by),
            "deleted_at": barangay_official.deleted_at,
            "deleted_by": str(barangay_official.deleted_by),
        })

    return {
        "message": "Barangay Captains fetched successfully!",
        "data": data
    }



# Get Specific Barangay Official
@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    barangay_official = db.query(BarangayOfficial).filter(BarangayOfficial.id == id,
                                                          BarangayOfficial.deleted_at == None).first()

    if barangay_official:
        # Convert image to base64
        with open(barangay_official.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        return {
            "message": f"Barangay official fetched successfully {barangay_official.id}",
            "data": {
                "id": barangay_official.id,
                "start_term": barangay_official.start_term,
                "end_term": barangay_official.end_term,
                "first_name": barangay_official.first_name,
                "middle_name": barangay_official.middle_name,
                "last_name": barangay_official.last_name,
                "suffix": barangay_official.suffix,
                "birthday": barangay_official.birthday,
                "email": barangay_official.email,
                "contact_no": barangay_official.contact_no,
                "position": barangay_official.position,
                "photo_path": encoded_image,  # Include base64-encoded image data
                "created_at": barangay_official.created_at,
                "created_by": barangay_official.created_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Information does not exist!")

UPLOADS_DIR = "images/BarangayOfficials"  # Define your folder directory path here

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
        start_term: str = Form(...),
        end_term: str = Form(...),
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

        barangay_official = BarangayOfficial(
            start_term=start_term,
            end_term=end_term,
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
        db.add(barangay_official)
        db.commit()

        data = {
            "start_term": barangay_official.start_term,
            "end_term": barangay_official.end_term,
            "first_name": barangay_official.first_name,
            "middle_name": barangay_official.middle_name,
            "last_name": barangay_official.last_name,
            "suffix": barangay_official.suffix,
            "birthday": barangay_official.birthday,
            "email": barangay_official.email,
            "contact_no": barangay_official.contact_no,
            "position": barangay_official.position,
            "photo_path": barangay_official.photo_path,
            "created_at": barangay_official.created_at,
            "created_by": barangay_official.created_by
        }

        return {
            "message": "Barangay Official Successfully Added!",
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

# Update Barangay Official
@router.put("/{id}")
async def update(id: UUID, request: BarangayOfficialSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")
        # Retrieve user id from the authenticated user
    userid = user.id
    barangay_official = db.query(BarangayOfficial).filter(BarangayOfficial.id == id,
                                                          BarangayOfficial.deleted_at == None).first()

    if barangay_official:
        # Update other fields
        barangay_official.first_name = request.first_name
        barangay_official.middle_name = request.middle_name
        barangay_official.last_name = request.last_name
        barangay_official.suffix = request.suffix
        barangay_official.birthday = request.birthday
        barangay_official.email = request.email
        barangay_official.contact_no = request.contact_no
        barangay_official.position = request.position
        barangay_official.start_term = request.start_term
        barangay_official.end_term = request.end_term

        # Handle photo update
        if request.photo_path:
            old_photo_path = barangay_official.photo_path

            # Save the new photo
            photo_path = save_photo(request.photo_path, UPLOADS_DIR)

            # Update the photo path
            barangay_official.photo_path = photo_path

            # Delete the old photo
            if old_photo_path and os.path.exists(old_photo_path):
                os.remove(old_photo_path)

        # Update other fields
        barangay_official.updated_at = datetime.now()
        barangay_official.updated_by = userid

        db.commit()

        return {
            "message": f"Barangay Official: {barangay_official.id} updated successfully",
            "data": {
                "first_name": barangay_official.first_name,
                "middle_name": barangay_official.middle_name,
                "last_name": barangay_official.last_name,
                "suffix": barangay_official.suffix,
                "birthday": barangay_official.birthday,
                "email": barangay_official.email,
                "contact_no": barangay_official.contact_no,
                "position": barangay_official.position,
                "start_term": barangay_official.start_term,
                "end_term": barangay_official.end_term,
                "created_at": barangay_official.created_at,
                "created_by": str(barangay_official.created_by),
                "updated_at": barangay_official.updated_at,
                "updated_by": str(barangay_official.updated_by)
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Barangay Official does not exist!")

def save_photo(photo_path, upload_dir):
    # Generate a unique filename for the uploaded photo
    file_extension = photo_path.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_extension}"

    # Save the photo to the specified directory
    save_path = os.path.join(upload_dir, filename)

    with open(save_path, "wb") as photo_file:
        photo_file.write(photo_path.file.read())

    return save_path

@router.delete("/{id}")
async def delete(id: UUID, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Retrieve the barangay official
    barangay_official = db.query(BarangayOfficial).filter(BarangayOfficial.id == id,
                                                          BarangayOfficial.deleted_at == None).first()

    user = db.query(User).filter(User.email == current_user.email).first()

    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    if barangay_official:
        # Get the file path from the barangay official data
        file_path = barangay_official.photo_path

        # Delete the image file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Update barangay official data to mark it as deleted
        barangay_official.deleted_at = datetime.now()
        barangay_official.deleted_by = userid
        db.commit()

        return {"message": "Barangay Official deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Information does not exist!")