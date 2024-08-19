from pydantic import BaseModel


class SBOMBase(BaseModel):
    name: str
    version: str
    project_id: int


class SBOMCreate(SBOMBase):
    pass


class SBOM(SBOMBase):
    id: int

    class Config:
        from_attributes = True
