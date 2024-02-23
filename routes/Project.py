from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Project import Project
from models.User import User
from schemas.Project import ProjectSchema
from schemas.User import UserSchema
from auth.Oauth2 import get_current_user
from datetime import datetime
from pydantic import UUID4
from sqlalchemy import or_

router = APIRouter(prefix="/projects", tags=["Project"])


# Get All Ordinances

@router.get("/get")
async def index(db: Session = Depends(get_db)):
    # Query all residents that are not marked as deleted
    projects = db.query(Project).filter(Project.deleted_at == None).all()
    data = []

    if projects:
        for project in projects:
            data.append({
                "id": project.id,
                "title": project.title,
                "projType ": project.projType,
                "description ": project.description,
                "duration  ": project.duration,
                "started  ": project.started,
                "budget  ": project.budget,
                "source   ": project.source,
                "created_at": project.created_at,
                "created_by": project.created_by,
                "updated_at": project.updated_at,
                "updated_by": project.updated_by
            })
        return {
            "message": "Projects fetched successfully",
            "data": data
       }
    else:
        raise HTTPException(status_code=404, detail="Projects not found")

@router.get("/getp")
async def index(
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)):

    # Calculate the offset based on the page and limit
    offset = (page - 1) * limit

    # Query residents with pagination and search
    query = db.query(Project).filter(Project.deleted_at == None)

    if search:
        # Use OR condition to search in multiple columns
        query = query.filter(
            or_(
                Project.title .ilike(f"%{search}%"),
                Project.projType .ilike(f"%{search}%"),
                Project.status .ilike(f"%{search}%"),
                Project.budget .ilike(f"%{search}%"),
                # Add more columns as needed
            )
        )

    projects = query.offset(offset).limit(limit).all()

    data = []

    if projects:
        for project in projects:
            data.append({
                "id": project.id,
                "title": project.title,
                "projType": project.projType,
                "description": project.description,
                "status": project.status,
                "duration": project.duration,
                "started": project.started,
                "budget": project.budget,
                "source": project.source,
                "created_at": project.created_at,
                "created_by": project.created_by,
                "updated_at": project.updated_at,
                "updated_by": project.updated_by
            })

        return {
            "message": "Projects fetched successfully",
            "data": data,
            "page": page,
            "limit": limit
        }
    else:
        raise HTTPException(status_code=404, detail="Projects not found")
@router.get("/deleted")
async def index(db: Session = Depends(get_db)):
    projects = db.query(Project).filter(Project.deleted_at != None).all()
    data = []
    if projects:
        for project in projects:
            data.append({
                "id": project.id,
                "title": project.title,
                "projType": project.projType,
                "description": project.description,
                "status": project.status,
                "duration": project.duration,
                "started": project.started,
                "budget": project.budget,
                "source": project.source,
                "created_at": project.created_at,
                "created_by": project.created_by,
                "updated_at": project.updated_at,
                "updated_by": project.updated_by
            })
        return {
            "message": "Projects fetched successfully",
            "data": data
        }
    else:
        return {
            "message": "No projects found",
            "data": []
        }

@router.post("/add")
async def store(request: ProjectSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")
    # Retrieve user id from the authenticated user
    userid = user.id

    # Check if resident with the same first_name already exists
    #resident = db.query(ResidentProfile).filter(ResidentProfile.first_name == request.first_name).first()
    #if resident:
        #raise HTTPException(status_code=400, detail=f"Resident with name '{request.first_name}' already exists!")

    try:
        # Create a new ResidentProfile instance
        project = Project(
            title=request.title,
            projType=request.projType,
            description=request.description,
            status=request.status,
            duration=request.duration,
            started=request.started,
            budget=request.budget,
            source=request.source,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(project)
        db.commit()

        # Return success message and data
        return {
            "message": "Resident successfully added!",
            "data": {
                "title": project.title,
                "projType": project.projType,
                "description": project.description,
                "duration": project.duration,
                "started": project.started,
                "budget": project.budget,
                "source": project.source,
                "created_at": project.created_at,
                "created_by": project.created_by
            }
        }
    except Exception as e:
        # Rollback and raise exception in case of an error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id, Project.deleted_at == None).first()

    if project:
        return {
            "message": f"Project: {project.id} fetched successfully!",
            "data": {
                "id": project.id,
                "title": project.title,
                "projType": project.projType,
                "description": project.description,
                "status": project.status,
                "duration": project.duration,
                "started": project.started,
                "budget": project.budget,
                "source": project.source,
                "created_at": project.created_at,
                "created_by": project.created_by,
                "updated_at": project.updated_at,
                "updated_by": project.updated_by,
                "deleted_at": project.deleted_at,
                "deleted_by": project.deleted_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Project does not exists!")


#addProj

@router.put("/{id}")
async def update(id: UUID4, request: ProjectSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == id, Project.deleted_at == None).first()
    user = db.query(User).filter(User.email == current_user.email).first()
    #Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")
    # Retrieve user id from the authenticated user
    userid = user.id

    if project:
        project.title = request.title
        project.projType = request.projType
        project.description = request.description
        project.status = request.status
        project.duration = request.duration
        project.started = request.started
        project.budget = request.budget
        project.source = request.source
        project.updated_at = datetime.now()
        project.updated_by = userid
        db.commit()

        return {
            "message": f"Resident: {project.id} updated successfully",
            "data": {
                "title ": project.title,
                "projType ": project.projType,
                "created_at": project.created_at,
                "created_by": project.created_by,
                "updated_at": project.updated_at,
                "updated_by": project.deleted_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Resident does not exists!")

@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == id, Project.deleted_at == None).first()
    user = db.query(User).filter(User.email == current_user.email).first()
    # Ensure user is authenticated
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")
    # Retrieve user id from the authenticated user
    userid = user.id

    if project:
        project.deleted_at = datetime.now()
        project.deleted_by = userid
        db.commit()
        return {
            "message": f"Resident: {project.id} deleted successfully!",
            "data": {
                   "deleted_at": project.deleted_at,
                   "deleted_by": project.deleted_by,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Resident does not exists!")