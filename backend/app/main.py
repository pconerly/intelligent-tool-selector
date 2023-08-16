import json
from os import path

from fastapi import FastAPI
from sqlalchemy.orm import Session
# from sqlalchemy.ext.declarative import declarative_base
from models import SessionLocal, ToolDB
from routes import router as tool_router
# from tool_fixtures import tool_fixtures

app = FastAPI()

current_directory = path.dirname(path.abspath(__file__))


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
