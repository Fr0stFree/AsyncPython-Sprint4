from models import UrlClick as UrlClickModel
from schemes.url_click import UrlClickCreate, UrlClickUpdate
from .base import RepositoryInterface


class UrlClickRepository(RepositoryInterface[UrlClickModel, UrlClickCreate, UrlClickUpdate]):
    pass


UrlClick = UrlClickRepository(UrlClickModel)
