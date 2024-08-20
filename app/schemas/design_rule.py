from pydantic import ConfigDict
from pydantic import BaseModel


class DesignRuleBase(BaseModel):
    name: str
    description: str = None
    project_id: int


class DesignRuleCreate(DesignRuleBase):
    pass


class DesignRule(DesignRuleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
