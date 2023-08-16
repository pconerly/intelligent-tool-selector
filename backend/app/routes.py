import json

from fastapi import APIRouter, Body, Depends, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from models import Tool, ToolDB, Prompt, PromptDB, get_db
from gpt_api import get_tools

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/tools", response_model=List[Tool])  # Note: You'd need to import List from typing
def read_tools(db: Session = Depends(get_db)):
    tools_db = db.query(ToolDB).filter(ToolDB.loggedIn == True).all()
    # Convert ORM objects to Pydantic models
    tools = [Tool.from_orm(tool) for tool in tools_db]
    return tools

# Endpoint to create a new tool
@router.post("/tools/")
def create_tool(tool: Tool, db: Session = Depends(get_db)):
    db_tool = ToolDB(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.post('/prompt')
def create_prompt(prompt: Prompt,  db: Session = Depends(get_db)):
    db_prompt = PromptDB(**prompt.dict())
    db.add(db_prompt)
    db.commit()

    tools_db = db.query(ToolDB).all()

    # Convert ORM objects to Pydantic models
    tools = [Tool.from_orm(tool) for tool in tools_db]

    tools_json = json.dumps([tool.dict() for tool in tools])

    recommended_tools = get_tools(prompt, tools_json)


    return {"recommended_tools": recommended_tools}
