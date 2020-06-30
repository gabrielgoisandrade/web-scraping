from functools import wraps
from typing import Callable

from pymongo.errors import PyMongoError, BulkWriteError, OperationFailure

from log import error


class DatabaseHelper:

    @staticmethod
    def operation(func: Callable) -> Callable:
        """
        Executa determinada operação, que contenham retorno.

        :param func: função que está sendo decorada.
        :return: função interna
        """

        @wraps(func)
        def inner(*args, **kwargs) -> Callable:
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

    @staticmethod
    def void_operation(func: Callable) -> Callable:
        """
        Executa determinada operação, que não tenham retorno.

        :param func: função que está sendo decorada.
        :return: função interna
        """

        @wraps(func)
        def inner(*args, **kwargs) -> None:
            try:
                func(*args, **kwargs)
            except BulkWriteError as e:
                error(e.__str__())
                raise BulkWriteError('Erro ao inserir os dados.')
            except OperationFailure as e:
                error(e.__str__())
                raise OperationFailure('Erro ao realizar a operação.')
            except TypeError as e:
                error(e.__str__())
                raise TypeError('Erro no tipo de dado.')
            finally:
                from database import conn
                conn.close()

        return inner
