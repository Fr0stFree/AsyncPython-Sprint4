from pydantic import BaseModel, UUID4, HttpUrl, Field


class UrlBase(BaseModel):
    full_url: str


class UrlCreate(UrlBase):
    pass


class UrlUpdate(UrlBase):
    pass


class UrlDBBase(UrlBase):
    id: UUID4
    full_url: str
    clicks: int

    class Config:
        orm_mode = True


class Url(UrlDBBase):
    pass


class UrlInDB(UrlDBBase):
    pass
