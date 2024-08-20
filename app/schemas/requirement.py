from pydantic import ConfigDict
from pydantic import BaseModel


class RequirementBase(BaseModel):
    name: str
    description: str = None
    project_id: int


class RequirementCreate(RequirementBase):
    pass


class Requirement(RequirementBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
