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
def create_prompt(prompt: str,  db: Session = Depends(get_db)):
    db_prompt = PromptDB(prompt=prompt)
    db.add(db_prompt)
    db.commit()

    tools_db = db.query(ToolDB).all()
    # Convert ORM objects to Pydantic models
    tools = [Tool.from_orm(tool) for tool in tools_db]

    tools_json = json.dumps([tool.dict() for tool in tools])

    print('tools', tools)

    recommended_tools = get_tools(prompt, tools_json)

    print('recommended_tools', recommended_tools)

    # make a request to open, given the tools and the prompt?


    return {"recommended_tools": recommended_tools}

# @router.get("/hello")
# def hello():
#     return Response("hello world! what the what")

# @router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
# def create_book(request: Request, book: Book = Body(...)):
#     book = jsonable_encoder(book)
#     new_book = request.app.database["books"].insert_one(book)
#     created_book = request.app.database["books"].find_one(
#         {"_id": new_book.inserted_id}
#     )

#     return created_book

# @router.get("/", response_description="List all books", response_model=List[Book])
# def list_books(request: Request):
#     books = list(request.app.database["books"].find(limit=100))
#     return books

# @router.get("/{id}", response_description="Get a single book by id", response_model=Book)
# def find_book(id: str, request: Request):
#     if (book := request.app.database["books"].find_one({"_id": id})) is not None:
#         return book
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

# @router.put("/{id}", response_description="Update a book", response_model=Book)
# def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
#     book = {k: v for k, v in book.dict().items() if v is not None}
#     if len(book) >= 1:
#         update_result = request.app.database["books"].update_one(
#             {"_id": id}, {"$set": book}
#         )

#         if update_result.modified_count == 0:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

#     if (
#         existing_book := request.app.database["books"].find_one({"_id": id})
#     ) is not None:
#         return existing_book

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

# @router.delete("/{id}", response_description="Delete a book")
# def delete_book(id: str, request: Request, response: Response):
#     delete_result = request.app.database["books"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         response.status_code = status.HTTP_204_NO_CONTENT
#         return response

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")
