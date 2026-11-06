from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SpaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=90)

class SpaceCreate(SpaceBase):
    pass

class SpaceResponse(SpaceBase):

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SpaceMemberAdd(BaseModel):
    username: str

class SpaceMemberResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)