import uuid
from typing import  List, Dict, Optional
from pydantic import BaseModel, Field

from sqlalchemy import create_engine, Column, String, Table, ForeignKey, Integer, JSON, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./sqlite.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# schemas:
# prompt -> tools


# Association table
tool_prompt_association = Table(
    "tool_prompt",
    Base.metadata,
    Column("tool_id", String, ForeignKey("tools.id")),
    Column("prompt_id", String, ForeignKey("prompts.id"))
)

class PromptDB(Base):
    __tablename__ = "prompts"
    id = Column(String, primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
    prompt = Column(String, index=True)
    tools = relationship("ToolDB", secondary=tool_prompt_association, back_populates="prompts")

class Prompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    prompt: str

# SQLAlchemy ORM model
class ToolDB(Base):
    __tablename__ = "tools"

    id = Column(String, primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=True)
    description = Column(String, nullable=True)
    loggedIn = Column(Boolean, nullable=True)
    inputParameters = Column(JSON, nullable=True)
    prompts = relationship("PromptDB", secondary=tool_prompt_association, back_populates="tools")

# Pydantic model
class Tool(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: Optional[str]
    description: Optional[str]
    loggedIn: bool
    inputParameters: List[Dict[str, str]]

    class Config:
        from_attributes = True

Base.metadata.create_all(bind=engine)
