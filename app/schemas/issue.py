from pydantic import BaseModel


class IssueBase(BaseModel):
    title: str
    description: str = None
    project_id: int


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int

    class Config:
        orm_mode = True
