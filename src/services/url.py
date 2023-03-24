from models import Url as UrlModel
from schemes.url import UrlCreate, UrlUpdate
from .base import RepositoryInterface


class UrlRepository(RepositoryInterface[UrlModel, UrlCreate, UrlUpdate]):
    pass


Url = UrlRepository(UrlModel)
