from typing import Optional
from uuid import UUID
import uuid
import os
from uuid import uuid4
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.database import get_db
from models.ClearancePermit import ClearancePermit
from models.User import User
from schemas.ClearancePermit import ClearancePermitSchema
from schemas.User import UserSchema
from auth.Oauth2 import get_current_user
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import UUID4
from uuid import UUID

router = APIRouter(prefix="/clearancespermits", tags=["Clearances and Permits"])

# Get All Clearance Permits
@router.get("/all")
async def get_all_clearance_permits(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    clearance_permits = db.query(ClearancePermit).filter(ClearancePermit.deleted_at == None).all()

    data = []

    for clearance_permit in clearance_permits:
        # Convert image to base64
        with open(clearance_permit.valid_id_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        data.append({
            "id": str(clearance_permit.id),
            "type_of_request": clearance_permit.type_of_request,
            "name_of_resident": clearance_permit.name_of_resident,
            "request": clearance_permit.request,
            "permit": clearance_permit.permit,
            "reason": clearance_permit.reason,
            "contact_no": clearance_permit.contact_no,
            "email": clearance_permit.email,
            "valid_id_path": encoded_image,
            "date_requested": clearance_permit.date_requested,
            "date_scheduled": clearance_permit.date_scheduled,
            "date_released": clearance_permit.date_released,
            "date_received": clearance_permit.date_received,
            "created_by": str(clearance_permit.created_by),
            "updated_at": clearance_permit.updated_at,
            "updated_by": str(clearance_permit.updated_by),
            "deleted_at": clearance_permit.deleted_at,
            "deleted_by": str(clearance_permit.deleted_by) if clearance_permit.deleted_by else None,
        })

        return  {
        "message": "Clearance/Permit fetched successfully!",
        "data": data
    }

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

        # Query clearance permits with pagination and search
        query = db.query(ClearancePermit).filter(ClearancePermit.deleted_at == None)

        if search:
            # Use OR condition to search in multiple columns
            query = query.filter(
                or_(
                    ClearancePermit.type_of_request.ilike(f"%{search}%"),
                    ClearancePermit.name_of_resident.ilike(f"%{search}%"),
                    ClearancePermit.request.ilike(f"%{search}%"),
                    # Add more columns as needed
                )
            )

        clearance_permits = query.offset(offset).limit(limit).all()

        data = []

        for clearance_permit in clearance_permits:
            # Convert image to base64
            with open(clearance_permit.valid_id_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            data.append({
                "id": str(clearance_permit.id),
                "type_of_request": clearance_permit.type_of_request,
                "name_of_resident": clearance_permit.name_of_resident,
                "request": clearance_permit.request,
                "permit": clearance_permit.permit,
                "reason": clearance_permit.reason,
                "contact_no": clearance_permit.contact_no,
                "email": clearance_permit.email,
                "valid_id_path": encoded_image,
                "date_requested": clearance_permit.date_requested,
                "date_scheduled": clearance_permit.date_scheduled,
                "date_released": clearance_permit.date_released,
                "date_received": clearance_permit.date_received,
                "created_by": str(clearance_permit.created_by),
                "updated_at": clearance_permit.updated_at,
                "updated_by": str(clearance_permit.updated_by),
                "deleted_at": clearance_permit.deleted_at,
                "deleted_by": str(clearance_permit.deleted_by) if clearance_permit.deleted_by else None,
            })

        return {
            "message": "Clearance/Permit fetched successfully!",
            "data": data,
            "page": page,
            "limit": limit
        }

# Get Specific Clearance and Permit
@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    clearance_permit = db.query(ClearancePermit).filter(ClearancePermit.id == id, ClearancePermit.deleted_at == None).first()

    if clearance_permit:
        # Convert image to base64
        with open(clearance_permit.valid_id_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        return {
            "message": f"ClearancePermit: {clearance_permit.id} fetched successfully!",
            "data": {
                "id": clearance_permit.id,
                "name_of_resident": clearance_permit.name_of_resident,
                "type_of_request": clearance_permit.type_of_request,
                "request": clearance_permit.request,
                "permit": clearance_permit.permit,
                "reason": clearance_permit.reason,
                "contact_no": clearance_permit.contact_no,
                "email": clearance_permit.email,
                "valid_id_path": encoded_image,  # Include base64-encoded image data
                "date_requested": clearance_permit.date_requested,
                "date_scheduled": clearance_permit.date_scheduled,
                "date_released": clearance_permit.date_released,
                "date_received": clearance_permit.date_received,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Clearance or Permit does not exists!")

UPLOADS_DIR = "clearances_permits/"  # Define your folder directory path here
@router.post("/add")
async def store(
        name_of_resident: str = Form(...),
        type_of_request: str = Form(...),
        request: str = Form(...),
        permit: str = Form(...),
        reason: str = Form(...),
        contact_no: str = Form(...),
        email: str = Form(...),
        valid_id_path: UploadFile = File(...),
        date_requested: str = Form(...),
        date_scheduled: str = Form(...),
        date_released: str = Form(...),
        date_received: str = Form(...),
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
        valid_id_photo_path = save_valid_id(valid_id_path, UPLOADS_DIR)

        clearance_permit = ClearancePermit(
            type_of_request=type_of_request,
            name_of_resident=name_of_resident,
            request=request,
            permit=permit,
            reason=reason,
            contact_no=contact_no,
            email=email,
            valid_id_path=valid_id_photo_path,
            date_requested=date_requested,
            date_scheduled=date_scheduled,
            date_released=date_released,
            date_received=date_received,
            created_at=datetime.now(),
            created_by=userid
            )
        db.add(clearance_permit)
        db.commit()

        data = {
            "type_of_request": clearance_permit.type_of_request,
            "name_of_resident": clearance_permit.name_of_resident,
            "request": clearance_permit.request,
            "reason": clearance_permit.reason,
            "contact_no": clearance_permit.contact_no,
            "email": clearance_permit.email,
            "date_requested": clearance_permit.date_requested,
            "date_scheduled": clearance_permit.date_scheduled,
            "date_released": clearance_permit.date_released,
            "date_received": clearance_permit.date_received,
            "valid_id_path": clearance_permit.valid_id_path,
            "created_at": clearance_permit.created_at,
            "created_by": clearance_permit.created_by
        }

        return {
            "message": "Clearance/ Permit Successfully Added!",
            "data": data
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def save_valid_id(valid_id_path, upload_dir):
    # Generate a unique filename for the uploaded image
    file_extension = valid_id_path.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_extension}"

    # Save the image to the specified directory
    save_path = os.path.join(upload_dir, filename)

    # Delete the existing file if it exists
    if os.path.exists(save_path):
        os.remove(save_path)

    with open(save_path, "wb") as image_file:
        image_file.write(valid_id_path.file.read())

    return save_path


@router.put("/update/{clearance_permit_id}")
async def update_clearance_permit(
    clearance_permit_id: UUID,  # Change the type to UUID
    name_of_resident: str = Form(...),
    type_of_request: str = Form(...),
    request: str = Form(...),
    permit: str = Form(...),
    reason: str = Form(...),
    contact_no: str = Form(...),
    email: str = Form(...),
    valid_id_path: UploadFile = File(...),
    date_requested: str = Form(...),
    date_scheduled: str = Form(...),
    date_released: str = Form(...),
    date_received: str = Form(...),
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
        # Retrieve the existing ClearancePermit from the database
        existing_clearance_permit = db.query(ClearancePermit).filter(
            ClearancePermit.id == clearance_permit_id,
            ClearancePermit.deleted_at == None  # Ensure not deleted
        ).first()

        # Check if the ClearancePermit exists
        if not existing_clearance_permit:
            raise HTTPException(status_code=404, detail="Clearance/Permit not found")

        # Update the existing ClearancePermit fields
        existing_clearance_permit.type_of_request = type_of_request
        existing_clearance_permit.name_of_resident = name_of_resident
        existing_clearance_permit.request = request
        existing_clearance_permit.permit = permit
        existing_clearance_permit.reason = reason
        existing_clearance_permit.contact_no = contact_no
        existing_clearance_permit.email = email

        # Save the uploaded image file
        valid_id_photo_path = save_valid_id(valid_id_path, UPLOADS_DIR)
        existing_clearance_permit.valid_id_path = valid_id_photo_path

        existing_clearance_permit.date_requested = date_requested
        existing_clearance_permit.date_scheduled = date_scheduled
        existing_clearance_permit.date_released = date_released
        existing_clearance_permit.date_received = date_received
        existing_clearance_permit.updated_at = datetime.now()
        existing_clearance_permit.updated_by = userid

        db.commit()

        data = {
            "type_of_request": existing_clearance_permit.type_of_request,
            "name_of_resident": existing_clearance_permit.name_of_resident,
            "request": existing_clearance_permit.request,
            "reason": existing_clearance_permit.reason,
            "contact_no": existing_clearance_permit.contact_no,
            "email": existing_clearance_permit.email,
            "date_requested": existing_clearance_permit.date_requested,
            "date_scheduled": existing_clearance_permit.date_scheduled,
            "date_released": existing_clearance_permit.date_released,
            "date_received": existing_clearance_permit.date_received,
            "valid_id_path": existing_clearance_permit.valid_id_path,
            "updated_at": existing_clearance_permit.updated_at,
            "updated_by": existing_clearance_permit.updated_by
        }

        return {
            "message": "Clearance/Permit Successfully Updated!",
            "data": data
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}")
async def delete(id: UUID, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Retrieve the barangay official
    clearance_permit = db.query(ClearancePermit).filter(ClearancePermit.id == id,
                                                          ClearancePermit.deleted_at == None).first()

    user = db.query(User).filter(User.email == current_user.email).first()

    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    if clearance_permit:
        # Get the file path from the barangay official data
        file_path = clearance_permit.valid_id_path

        # Delete the image file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Update clearance/permit data to mark it as deleted
        clearance_permit.deleted_at = datetime.now()
        clearance_permit.deleted_by = userid
        db.commit()

        return {"message": "Clearance/Permit deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Clearance/Permit does not exist!")



