import os
import io
import logging
from sqlalchemy import or_
import uuid
from typing import Optional
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from config.database import get_db
from models.Ordinance import Ordinance
from models.User import User
from schemas.Ordinance import OrdinanceSchema
from schemas.User import UserSchema
from auth.Oauth2 import get_current_user
from datetime import datetime
from pydantic import UUID4
from uuid import UUID
from fastapi.responses import JSONResponse
from urllib.parse import unquote
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/ordinances", tags=["Ordinance"])


# Get All Ordinances
@router.get("/all")
async def get_all_ordinances(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    ordinances = db.query(Ordinance).filter(Ordinance.deleted_at == None).all()
    data = []

    if ordinances:
        for ordinance in ordinances:
            file_path = ordinance.file  # Assuming 'file' is the path to the saved file

            data.append({
                "id": str(ordinance.id),
                "title": ordinance.title,
                "author": ordinance.author,
                "description": ordinance.description,
                "file_path": file_path,  # Include the file path in the response
            })

        response_data = {
            "message": "Ordinances fetched successfully",
            "data": data
        }

        return JSONResponse(content=response_data, status_code=200)
    else:
        response_data = {
            "message": "No ordinances found",
            "data": []
        }

        return JSONResponse(content=response_data, status_code=404)

# Add a route to serve the files
@router.get("/get_file/{file_name}")
async def get_file(file_name: str):
    # URL decode the file name
    decoded_file_name = unquote(file_name)

    # Log the decoded file name and constructed file path
    logging.info(f"Decoded file name: {decoded_file_name}")

    file_path = os.path.join(UPLOADS_DIR, decoded_file_name)

    # Log the constructed file path
    logging.info(f"Constructed file path: {file_path}")

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Serve the file using FileResponse
    return FileResponse(file_path, filename=decoded_file_name)

#getp
@router.get("/getp")
async def get_paged_ordinances(
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    # Calculate the offset based on the page and limit
    offset = (page - 1) * limit

    # Query ordinances with pagination and search
    query = db.query(Ordinance).filter(Ordinance.deleted_at == None)

    if search:
        # Use OR condition to search in multiple columns
        query = query.filter(
            or_(
                Ordinance.title.ilike(f"%{search}%"),
                Ordinance.author.ilike(f"%{search}%"),
                Ordinance.description.ilike(f"%{search}%"),
                # Add more columns as needed
            )
        )

    ordinances = query.offset(offset).limit(limit).all()

    data = []

    if ordinances:
        for ordinance in ordinances:
            file_path = ordinance.file  # Assuming 'file' is the path to the saved file

            data.append({
                "id": str(ordinance.id),
                "title": ordinance.title,
                "author": ordinance.author,
                "description": ordinance.description,
                "file_path": file_path,  # Include the file path in the response
                "created_at": ordinance.created_at.strftime("%Y-%m-%d %H:%M:%S") if ordinance.created_at else None,
                "created_by": str(ordinance.created_by),
                "updated_at": ordinance.updated_at.strftime("%Y-%m-%d %H:%M:%S") if ordinance.updated_at else None,
                "updated_by": str(ordinance.updated_by),
                "deleted_at": ordinance.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if ordinance.deleted_at else None,
                "deleted_by": str(ordinance.deleted_by),
            })

        response_data = {
            "message": "Ordinances fetched successfully!",
            "data": data,
            "page": page,
            "limit": limit
        }

        return response_data
    else:
        raise HTTPException(status_code=404, detail="No ordinances found!")

#Get All Deleted Ordinances

@router.get("/all")
async def get_all_ordinances(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    ordinances = db.query(Ordinance).filter(Ordinance.deleted_at != None).all()
    data = []

    if ordinances:
        for ordinance in ordinances:
            file_path = ordinance.file  # Assuming 'file' is the path to the saved file

            data.append({
                "id": str(ordinance.id),
                "title": ordinance.title,
                "author": ordinance.author,
                "description": ordinance.description,
                "file_path": file_path,  # Include the file path in the response
            })

        response_data = {
            "message": "Ordinances fetched successfully",
            "data": data
        }

        return JSONResponse(content=response_data, status_code=200)
    else:
        response_data = {
            "message": "No ordinances found",
            "data": []
        }

        return JSONResponse(content=response_data, status_code=404)

@router.get("/view_file/{id}")
async def view_file(id: UUID, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    ordinance = db.query(Ordinance).filter(Ordinance.id == id, Ordinance.deleted_at == None).first()

    if ordinance:
        file_path = ordinance.file  # Assuming 'file' is the path to the saved file

        # Open the file and return it as a streaming response
        with open(file_path, "rb") as file:
            content = file.read()
            return StreamingResponse(io.BytesIO(content), media_type="application/pdf")  # Adjust media_type based on file type

    else:
        raise HTTPException(status_code=404, detail="Ordinance not found!")

# Add Ordinance with file upload
UPLOADS_DIR = "files/"  # Define your folder directory path here

@router.post("/add")
async def store_files(
        title: str = Form(...),
        author: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
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
        # Save the uploaded file
        uploaded_file_path = save_uploaded_file(file, UPLOADS_DIR)

        ordinance = Ordinance(
            title=title,
            author=author,
            description=description,
            file=uploaded_file_path,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(ordinance)
        db.commit()

        data = {
            "title": ordinance.title,
            "author": ordinance.author,
            "description": ordinance.description,
            "file": ordinance.file,
            "created_at": ordinance.created_at,
            "created_by": ordinance.created_by
        }

        return {
            "message": "Ordinance Successfully Added!",
            "data": data
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def save_uploaded_file(file_path: UploadFile, upload_dir: str):
    # Generate a unique filename for the uploaded file
    file_extension = file_path.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"

    # Save the file to the specified directory
    save_path = os.path.join(upload_dir, filename)

    with open(save_path, "wb") as uploaded_file:
        uploaded_file.write(file_path.file.read())

    return save_path

# Update an Ordinance
@router.put("/update/{id}")
async def update_ordinance(
        id: UUID,
        title: str = Form(...),
        author: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user.email).first()

    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    ordinance = db.query(Ordinance).filter(Ordinance.id == id, Ordinance.deleted_at == None).first()

    if ordinance:
        try:
            # Delete the existing file
            if os.path.exists(ordinance.file):
                os.remove(ordinance.file)

            # Save the new file
            uploaded_file_path = save_uploaded_file(file, UPLOADS_DIR)

            # Update ordinance data
            ordinance.title = title
            ordinance.author = author
            ordinance.description = description
            ordinance.file = uploaded_file_path
            ordinance.updated_at = datetime.now()
            ordinance.updated_by = userid

            db.commit()

            data = {
                "id": str(ordinance.id),
                "title": ordinance.title,
                "author": ordinance.author,
                "description": ordinance.description,
                "file_path": ordinance.file,
                "updated_at": ordinance.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_by": str(ordinance.updated_by),
            }

            return {
                "message": f"Ordinance {str(ordinance.id)} updated successfully!",
                "data": data
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="Ordinance not found!")
# Delete Ordinance
@router.delete("/{id}")
async def delete_ordinance(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve the ordinance
    ordinance = db.query(Ordinance).filter(Ordinance.id == id).first()

    user = db.query(User).filter(User.email == current_user.email).first()

    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    # Retrieve user id from the authenticated user
    userid = user.id

    if ordinance:
        # Get the file path from the ordinance data
        file_path = ordinance.file

        # Delete the file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete the ordinance data
        db.delete(ordinance)
        db.commit()

        return {"message": "Ordinance deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Ordinance not found")
