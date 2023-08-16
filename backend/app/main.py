import json
from os import path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from models import SessionLocal, ToolDB
from routes import router as tool_router

current_directory = path.dirname(path.abspath(__file__))

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Create a new session
    session = SessionLocal()


    # delete all tools:
    session.query(ToolDB).delete()
    session.commit()

    # Check if data already exists (to avoid inserting duplicates)
    # Here, we just check if there's any tool in the database

    fixtures_path = path.join(current_directory, '..', 'tool_fixtures.json')
    with open(fixtures_path, 'r') as f:
        tool_fixtures = json.load(f)

    tool_exists = session.query(ToolDB).first()
    if not tool_exists:
        for tool_data in tool_fixtures:
            print('tool_data', tool_data)
            tool = ToolDB(**tool_data)
            session.add(tool)
        
        session.commit()

    # Close the session
    session.close()



# Dependency to get the database session
app.include_router(tool_router, tags=["tools"])
