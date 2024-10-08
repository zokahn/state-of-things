from pydantic import ConfigDict
from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Project(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
