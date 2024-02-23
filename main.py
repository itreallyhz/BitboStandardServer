from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import event

import models
from routes import (ResidentProfile, BarangayOfficial, Personnel, Ordinance, Configuration,
                    User, Authentication, Project, ClearancePermit, Incident)

from config.database import engine

app = FastAPI(
    title="Bitbo Basic",
    version="0.0.1"
)

# Allow all origins during development. In production, specify your actual frontend URL.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# seeding Courses data// Makes the system avoid any problems in backend
# ----------------------------------------------------------------------------------------------------------------------
data = {

    #"householdprofiles": [
        #{
            #"street": "Acacia St.",
           # "lot": "L22",
           # "created_at": "2023-12-26 12:02:22",
           # "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
       # }
  #  ],
    "configurations":[
        {
            "region": "region A",
            "city_municipality": "City A",
            "barangay": "Barangay A",
            "created_at": "2023-12-26 12:02:22",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        }

    ]

}


def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in data and len(data[tablename]) > 0:
        connection.execute(target.insert(), data[tablename])


event.listen(models.ResidentProfile.ResidentProfile.__table__, 'after_create', initialize_table)
# ----------------------------------------------------------------------------------------------------------------------


@app.on_event("startup")
def configure():
    models.Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Welcome"])
async def root() -> dict:
    return {
        "message": f"Welcome to {app.title} v{app.version}."
    }


# include the routing for all the api
app.include_router(ResidentProfile.router)
app.include_router(BarangayOfficial.router)
app.include_router(Personnel.router)
app.include_router(Ordinance.router)
app.include_router(Configuration.router)
app.include_router(User.router)
app.include_router(Authentication.router)
app.include_router(Project.router)
app.include_router(ClearancePermit.router)
app.include_router(Incident.router)