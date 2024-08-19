from pydantic import BaseModel


class DesignRuleBase(BaseModel):
    name: str
    description: str = None
    project_id: int


class DesignRuleCreate(DesignRuleBase):
    pass


class DesignRule(DesignRuleBase):
    id: int

    class Config:
        from_attributes = True
