from typing import Optional, Union, List

from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import OperationFailure, BulkWriteError

from database.connectionDatabase import ConnectionDatabase
from log import info, error, critical
from .helper import helper


class OperationsDatabase:
    __CONN = ConnectionDatabase().get_connection

    @classmethod
    def __database(cls, db_name: Optional[str] = 'scraping') -> Database:
        """
        Retorna o banco de dados padrão, caso o nenhum valor seja passado em 'db_name'.\n
        Senão, um novo banco de dados será criado e retornado.\n

        :param db_name: nome do banco de dados a ser criado, ou retornado.
        :raise OperationFailure: falha ao criar o banco de dados.
        :return: banco de dados criado.
        """

        if db_name not in cls.__CONN.list_database_names():
            try:
                db: Database = cls.__CONN[db_name]
                info(f'Database {db_name} criado.')
                return db
            except OperationFailure as e:
                error(f'Erro ao criar o database: {e.__str__()}')
        return cls.__CONN.get_database(db_name)

    def __collection(self, is_current_occurrences: Optional[bool] = False) -> Collection:
        """
        Retorna a collection especificada, caso exista.\n
        Senão, uma nova será criada e retornada.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param is_current_occurrences: boolean para identificar qual collection será criada, ou retornada.
        :return: collection criada ou selecionada.
        """

        db: Database = self.__database()

        coll_name: str = 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        if coll_name not in db.list_collection_names():
            try:
                db.create_collection(coll_name)
                info(f'Collection {coll_name} criada.')
            except OperationFailure as e:
                error(f'Erro ao criar a collection: {e.__str__()}')
        return db.get_collection(coll_name)

    @helper.operation
    def count_documents(self, is_current_occurrences: Optional[bool] = False,
                        data_filter: Optional[dict] = None) -> int:
        """
        Retorna a quantidade de dados da collection.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param is_current_occurrences: boolean para identificar em qual collection será realizada a operação.
        :param data_filter: dado a ser filtrado.
        :return: quantidade de dados.
        """

        coll: Collection = self.__collection(is_current_occurrences)

        if data_filter: return coll.count_documents(data_filter)
        return coll.count_documents({})

    @helper.operation
    def get_collection_datas(self, is_current_occurrences: Optional[bool] = False,
                             data_filter: Optional[dict] = None) -> Union[List[dict], dict]:
        """
        Retorna os dados da collection especificada.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param is_current_occurrences: boolean para identificar em qual collection a operação será realizada.
        :param data_filter: dado a ser filtrado.
        :return: dados da collection.
        """

        coll: Collection = self.__collection(is_current_occurrences)

        if data_filter: return coll.find_one(data_filter)
        return list(coll.find({}))

    @helper.operation
    def insert(self, data: Union[List[dict], dict], is_current_occurrences: Optional[bool] = False) -> None:
        """
        Insersão de um, ou mais dados na collection especificada.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param data: dados a serem inseridos.
        :param is_current_occurrences: boolean para identificar em qual collection a operação será realizada.
        """

        coll: Collection = self.__collection(is_current_occurrences)
        coll.insert_many(data) if type(data) is list else coll.insert_one(data)

    def update_datas(self, old_datas: List[dict], new_datas: List[dict],
                     is_current_occurrences: Optional[bool] = False) -> None:
        """
        Atualiza os dados de uma determinada collection.

        :param is_current_occurrences: boolean para identificar se a collection a ser atualizada será a com os dados do ano
                atual, ou do ano passado.
        :param old_datas: dados dados a serem atualizadods.
        :param new_datas: dados a serem inseridos.
        """

        coll: Collection = self.__collection(is_current_occurrences)

        try:
            [coll.update_one(old_datas[value], {'$set': new_datas[value]}) for value in range(len(new_datas))]
            info('Dados atualizados com sucesso.')
        except BulkWriteError as e:
            critical(f'Erro ao atualizar dados. Detalhes: {e.details}')
        finally:
            self.__CONN.close()
