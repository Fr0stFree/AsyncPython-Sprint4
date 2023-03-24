from models import User as UserModel
from schemes.user import UserCreate, UserUpdate
from .base import RepositoryInterface


class UserRepository(RepositoryInterface[UserModel, UserCreate, UserUpdate]):
    pass


User = UserRepository(UserModel)
