from pydantic import BaseModel, UUID4, HttpUrl, Field


class UrlBase(BaseModel):
    full_url: HttpUrl


class UrlCreate(UrlBase):
    pass


class UrlUpdate(UrlBase):
    pass


class UrlDBBase(UrlBase):
    id: UUID4
    full_url: HttpUrl
    clicks: int

    class Config:
        orm_mode = True


class Url(UrlDBBase):
    pass


class UrlInDB(UrlDBBase):
    pass
