
from pydantic import BaseModel, ConfigDict


class SkillCreate(BaseModel):
    name: str


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
