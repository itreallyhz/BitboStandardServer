from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import DataError, IntegrityError
from sqlalchemy.orm import Session

from auth.Oauth2 import get_current_user
from config.database import get_db
from models.Configuration import Configuration
from models.User import User
from schemas.User import UserSchema
from schemas.Configuration import ConfigurationSchema
from datetime import datetime
from pydantic import UUID4

router = APIRouter(prefix="/configurations", tags=["Configuration"])

#Get all configurations
@router.get("/")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Configurations db
    configurations = db.query(Configuration).filter(Configuration.deleted_at == None).all()
    data = []
    if configurations:
        for configuration in configurations:
            data.append({
                "id": configuration.id,
                "region": configuration.region,
                "province": configuration.province,
                "municipality": configuration.municipality,
                "district": configuration.district,
                "barangay": configuration.barangay,
                "created_at": configuration.created_at,
                "created_by": configuration.created_by,
                "updated_at": configuration.updated_at,
                "updated_by": configuration.updated_by
            })
        return {
            "message": "All configurations successfully fetched!",
            "data": data
       }
    else:
        raise HTTPException(status_code=404, detail=f"Configuration data does not exists!")

#Get deleted configurations
@router.get("/deleted")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Configurations db
    configurations = db.query(Configuration).filter(Configuration.deleted_at != None).all()
    data = []
    if configurations:
        for configuration in configurations:
            data.append({
                "id": configuration.id,
                "region": configuration.region,
                "province": configuration.province,
                "municipality": configuration.municipality,
                "district": configuration.district,
                "barangay": configuration.barangay,
                "created_at": configuration.created_at,
                "created_by": configuration.created_by,
                "updated_at": configuration.updated_at,
                "updated_by": configuration.updated_by
            })
        return {
            "message": "All configurations successfully fetched!",
            "data": data
       }
    else:
        raise HTTPException(status_code=404, detail=f"Configuration data does not exists!")

#Get a specific configuration
@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    configuration = db.query(Configuration).filter(Configuration.id == id, Configuration.deleted_at == None).first()

    if configuration:
        return {
            "message": f"Configuration:{configuration.id} successfully fetched!",
            "data": {
                "id": configuration.id,
                "region": configuration.region,
                "province": configuration.province,
                "municipality": configuration.municipality,
                "district": configuration.district,
                "barangay": configuration.barangay,
                "created_at": configuration.created_at,
                "created_by": configuration.created_by,
                "updated_at": configuration.updated_at,
                "updated_by": configuration.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Configuration does not exists!")

#Add a configuration
@router.post("/add")
async def store(request: ConfigurationSchema, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id

    #To check if data already exists
    #existing_configuration = db.query(Configuration).filter_by(
        #region=request.region,
        #province=request.province,
        #municipality=request.municipality,
        #district=request.district,
        #barangay=request.barangay
        #).all()

    #if existing_configuration:
        #raise HTTPException(status_code=409, detail="The configuration data already exists!")

    try:
        configuration = Configuration(
            region=request.region,
            province=request.province,
            municipality=request.municipality,
            district=request.district,
            barangay=request.barangay,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(configuration)
        db.commit()
        return {
                "message": "Configuration successfully added!",
                "data": {
                    "region": configuration.region,
                    "district": configuration.region,
                    "municipality": configuration.municipality,
                    "district": configuration.district,
                    "barangay": configuration.barangay,
                    "created_at": configuration.created_at,
                    "created_by": configuration.created_by
            }
            }
    except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

#Delete a configuration
@router.delete("/{id}")
async def delete(id: UUID4, db: Session= Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    configuration = db.query(Configuration).filter(Configuration.id == id, Configuration.deleted_at == None).first()
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id

    if configuration:
        configuration.deleted_at = datetime.now()
        configuration.deleted_by = userid
        db.commit()
        return{"message": "Configuration successfully deleted!"}

    else:
        raise HTTPException(status_code=404, detail=f"Data does not exists.")
