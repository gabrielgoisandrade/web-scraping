from functools import wraps
from typing import Callable

from pymongo.errors import PyMongoError

from log import error


class DatabaseHelper:

    @staticmethod
    def operation(func: Callable) -> Callable:
        """
        Executa determinada operação.

        :param func: função que está sendo decorada.
        :return: função interna
        """

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except PyMongoError as e:
                error(e.__str__())
                raise PyMongoError('Erro ao executar a operação.')
            except TypeError as e:
                error(e.__str__())
                raise
            finally:
                from database import conn
                conn.close()
            return func(*args, **kwargs)

        return inner
