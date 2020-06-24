from typing import Type

from model.base_crud_dao import BaseCrudDao
from model.user import User


class UserDao(BaseCrudDao):

    def get_odm(self) -> Type[User]:
        return User
