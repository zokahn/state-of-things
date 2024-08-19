from pydantic import BaseModel


class ProjectGoalBase(BaseModel):
    name: str
    description: str = None
    project_id: int


class ProjectGoalCreate(ProjectGoalBase):
    pass


class ProjectGoal(ProjectGoalBase):
    id: int

    class Config:
        from_attributes = True
