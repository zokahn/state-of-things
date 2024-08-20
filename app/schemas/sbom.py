from pydantic import ConfigDict
from pydantic import BaseModel


class SBOMBase(BaseModel):
    name: str
    version: str
    project_id: int


class SBOMCreate(SBOMBase):
    pass


class SBOM(SBOMBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
