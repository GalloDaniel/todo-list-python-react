from pydantic import BaseModel, field_validator, FieldValidationInfo

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool

class TodoCreate(TodoBase):
    title: str
    description: str
    completed: bool

    @field_validator("title", "description")
    @classmethod
    def not_empty(cls, v: str, info: FieldValidationInfo) -> str:
        if not v.strip():
            raise ValueError(f"O campo '{info.field_name}' é obrigatório e não pode estar vazio.")
        return v

class TodoUpdate(TodoBase):
    pass

class TodoOut(TodoBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    username: str
    password: str
