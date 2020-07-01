from typing import Optional, Union, List

from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import OperationFailure

from src.database import ConnectionDatabase
from src.log import info, error
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
    def __count_documents(self, is_current_occurrences: Optional[bool] = False,
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
    def __get_collection_datas(self, is_current_occurrences: Optional[bool] = False,
                               data_filter: Optional[dict] = None,
                               order: Optional[str] = '_id',
                               is_ascending: Optional[bool] = False) -> Union[List[dict], dict]:
        """
        Retorna os dados da collection especificada.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param is_current_occurrences: boolean para identificar em qual collection a operação será realizada.
        :param data_filter: dado a ser filtrado.
        :param order: forma que o dado será ordenado.
        :param is_ascending: boolean para identificar se os dados virão na ordem crescente ou descrescente.
        :return: dados da collection.
        """

        coll: Collection = self.__collection(is_current_occurrences)

        if data_filter: return coll.find_one(data_filter)
        return list(coll.find({}).sort(order, ASCENDING if is_ascending else DESCENDING))

    @helper.void_operation
    def __update_datas(self, new_datas: List[dict], is_current_occurrences: Optional[bool] = False) -> None:
        """
        Atualização de dados de uma determinada collection.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param is_current_occurrences: boolean para identificar em qual collection a operação será realizada.
        :param new_datas: dados a serem inseridos.
        """

        coll: Collection = self.__collection(is_current_occurrences)

        current_datas: List[dict] = helper.remove_element(
            self.__get_collection_datas(is_current_occurrences, is_ascending=True), '_id')

        new: List[dict] = [new_datas[value] for value in range(len(new_datas)) if
                           current_datas[value] != new_datas[value]]

        old: List[dict] = [current_datas[value] for value in range(len(new_datas)) if
                           current_datas[value] != new_datas[value]]

        if len(new) != 0:
            info(f'Iniciando atualização de {len(new)} dado(s) na collection '
                 f'{"current_occurrences" if is_current_occurrences else "last_occurrences"}.')

            for values in range(len(new)): coll.update_one(old[values], {'$set': new[values]})
            info("Dados atualizados com sucesso.")
        else:
            info('Não há dados a serem atualizados.')

    @helper.void_operation
    def insert(self, data: List[dict], is_current_occurrences: Optional[bool] = False) -> None:
        """
        Insersão de novos dados em determinada collection, caso não haja dados inseridos na mesma.\n
        Senão, haverá uma atualização nos dados existentes.\n

        >>> 'current_occurrences' if is_current_occurrences else 'last_occurrences'

        :param data: dados a serem inseridos.
        :param is_current_occurrences: boolean para identificar em qual collection a operação será realizada.
        """

        coll: Collection = self.__collection(is_current_occurrences)

        if self.__count_documents(is_current_occurrences) == 0:
            info(f'Insersão de {len(data)} novo(s) dado(s) na collection '
                 f'{"current_occurrences" if is_current_occurrences else "last_occurrences"}.')
            coll.insert_many(data)
        else:
            self.__update_datas(data, is_current_occurrences)