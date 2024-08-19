from pydantic import BaseModel


class RequirementBase(BaseModel):
    name: str
    description: str = None
    project_id: int


class RequirementCreate(RequirementBase):
    pass


class Requirement(RequirementBase):
    id: int

    class Config:
        from_attributes = True
