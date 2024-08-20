from pydantic import ConfigDict
from pydantic import BaseModel


class IssueBase(BaseModel):
    title: str
    description: str = None
    project_id: int


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class IssueUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    project_id: int | None = None
