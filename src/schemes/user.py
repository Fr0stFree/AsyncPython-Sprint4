from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserDBBase(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class User(UserDBBase):
    pass


class UserInDB(UserDBBase):
    pass
