from typing import Optional
from uuid import UUID
import uuid
import os
import base64

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.database import get_db
from models.Incident import Incident
from models.User import User
from schemas.Incident import IncidentSchema
from schemas.User import UserSchema
from auth.Oauth2 import get_current_user
from datetime import datetime
from pydantic import UUID4

router = APIRouter(prefix="/incidents", tags=["Incident"])


# Get All Incidents
@router.get("/all")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    incidents = db.query(Incident).filter(Incident.deleted_at == None).all()

    data = []

    for incident in incidents:
        # Convert image to base64
        with open(incident.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(incident.id),
            "case_title": incident.case_title,
            "case_description": incident.case_description,
            "complainant": incident.complainant,
            "witness": incident.witness,
            "officer": incident.officer,
            "subject_complaint": incident.subject_complaint,
            "place": incident.place,
            "happened": incident.happened,
            "status": incident.status,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(incident.created_by),
            "updated_at": incident.updated_at,
            "updated_by": str(incident.updated_by),
            "deleted_at": incident.deleted_at,
            "deleted_by": str(incident.deleted_by),
        })

    return {
        "message": "Incident fetched successfully!",
        "data": data
    }

# Get all Incidents || Pagination
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
    query = db.query(Incident).filter(Incident.deleted_at == None)

    if search:
        # Use OR condition to search in multiple columns
        query = query.filter(
            or_(
                Incident.case_title.ilike(f"%{search}%"),
                Incident.happened.ilike(f"%{search}%"),
                Incident.complainant.ilike(f"%{search}%"),
                # Add more columns as needed
            )
        )

    incidents = query.offset(offset).limit(limit).all()

    data = []

    for incident in incidents:
        # Convert image to base64
        with open(incident.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(incident.id),
            "case_title": incident.case_title,
            "case_description": incident.case_description,
            "complainant": incident.complainant,
            "witness": incident.witness,
            "officer": incident.officer,
            "subject_complaint": incident.subject_complaint,
            "place": incident.place,
            "happened": incident.happened,
            "status": incident.status,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(incident.created_by),
            "updated_at": incident.updated_at,
            "updated_by": str(incident.updated_by),
            "deleted_at": incident.deleted_at,
            "deleted_by": str(incident.deleted_by),
        })

    return {
        "message": "Incident fetched successfully!",
        "data": data,
        "page": page,
        "limit": limit
    }

# Get All Deleted Barangay Officials
@router.get("/deleted")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    incidents = db.query(Incident).filter(Incident.deleted_at != None).all()

    data = []

    for incident in incidents:
        # Convert image to base64
        with open(incident.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(incident.id),
            "case_title": incident.case_title,
            "case_description": incident.case_description,
            "complainant": incident.complainant,
            "witness": incident.witness,
            "officer": incident.officer,
            "subject_complaint": incident.subject_complaint,
            "place": incident.place,
            "happened": incident.happened,
            "status": incident.status,
            "photo_path": encoded_image,  # Include base64-encoded image data
            "created_by": str(incident.created_by),
            "updated_at": incident.updated_at,
            "updated_by": str(incident.updated_by),
            "deleted_at": incident.deleted_at,
            "deleted_by": str(incident.deleted_by),
        })

    return {
        "message": "Incident fetched successfully!",
        "data": data
    }



# Get Specific Barangay Official
@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    incident = db.query(Incident).filter(Incident.id == id,
                                                          Incident.deleted_at == None).first()

    if incident:
        # Convert image to base64
        with open(incident.photo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        return {
            "message": f"Incident fetched successfully {incident.id}",
            "data": {
                "id": incident.id,
                "case_title": incident.case_title,
                "case_description": incident.case_description,
                "complainant": incident.complainant,
                "witness": incident.witness,
                "officer": incident.officer,
                "subject_complaint": incident.subject_complaint,
                "place": incident.place,
                "happened": incident.happened,
                "status": incident.status,
                "photo_path": encoded_image,  # Include base64-encoded image data
                "created_at": incident.created_at,
                "created_by": incident.created_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Information does not exist!")

UPLOADS_DIR = "images/Incidents"  # Define your folder directory path here

@router.post("/add")
async def store(
        case_title: str = Form(...),
        case_description: str = Form(...),
        complainant: str = Form(...),
        witness: str = Form(...),
        officer: str = Form(...),
        subject_complaint: str = Form(...),
        place: str = Form(...),
        happened: str = Form(...),
        status: str = Form(...),
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

        incident = Incident(
            case_title=case_title,
            case_description=case_description,
            complainant=complainant,
            witness=witness,
            officer=officer,
            subject_complaint=subject_complaint,
            place=place,
            happened=happened,
            status=status,
            photo_path=profile_photo_path,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(incident)
        db.commit()

        data = {
            "case_title": incident.case_title,
            "case_description": incident.case_description,
            "complainant": incident.complainant,
            "witness": incident.witness,
            "officer": incident.officer,
            "subject_complaint": incident.subject_complaint,
            "place": incident.place,
            "happened": incident.happened,
            "status": incident.status,
            "photo_path": incident.photo_path,
            "created_at": incident.created_at,
            "created_by": incident.created_by
        }

        return {
            "message": "Incident Successfully Added!",
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

# Update Incident
@router.put("/{id}")
async def update(id: UUID, request: IncidentSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")
        # Retrieve user id from the authenticated user
    userid = user.id
    incident = db.query(Incident).filter(Incident.id == id,
                                                          Incident.deleted_at == None).first()

    if incident:
        incident.case_title = request.case_title
        incident.case_description = request.case_description
        incident.complainant = request.complainant
        incident.witness = request.witness
        incident.officer = request.officer
        incident.subject_complaint = request.subject_complaint
        incident.place = request.place
        incident.happened = request.happened
        incident.status = request.status
        incident.photo_path = request.photo_path
        incident.updated_at = datetime.now()
        incident.updated_by = userid

        db.commit()

        return {
            "message": f"Incident: {incident.id} updated successfully",
            "data": {
                "case_title": incident.case_title,
                "case_description": incident.case_description,
                "complainant": incident.complainant,
                "witness": incident.witness,
                "officer": incident.officer,
                "subject_complaint": incident.subject_complaint,
                "place": incident.place,
                "happened": incident.happened,
                "status": incident.status,
                "created_at": incident.created_at,
                "created_by": str(incident.created_by),
                "updated_at": incident.updated_at,
                "updated_by": str(incident.updated_by)
            }
        }
    else:
        raise HTTPException(status_code=404, detail="incident does not exist!")

@router.delete("/{id}")
async def delete(id: UUID, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Retrieve the barangay official
    incident = db.query(Incident).filter(Incident.id == id,
                                                          Incident.deleted_at == None).first()

    user = db.query(User).filter(User.email == current_user.email).first()

    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    if incident:
        # Get the file path from the barangay official data
        file_path = incident.photo_path

        # Delete the image file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Update barangay official data to mark it as deleted
        incident.deleted_at = datetime.now()
        incident.deleted_by = userid
        db.commit()

        return {"message": "Incident Official deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Information does not exist!")