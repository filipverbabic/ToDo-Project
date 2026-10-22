from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str | None = Field(default = None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None

class TodoResponse(TodoBase):
    id: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)