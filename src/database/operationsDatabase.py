from typing import Optional, Union, List

from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import OperationFailure

from src.database import (remove_element, void_operation, operation)
from src.database.connectionDatabase import ConnectionDatabase
from src.log import info, error


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

    def collection(self, is_current_occurrences: Optional[bool] = False) -> Collection:
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

    @operation
    def count_documents(self, collection: Collection, data_filter: Optional[dict] = None) -> int:
        """
        Retorna a quantidade de dados da collection.

        :param collection: collection onde a quantidade de documents será retornada.
        :param data_filter: dado a ser filtrado.
        :return: quantidade de dados.
        """

        return collection.count_documents(data_filter) if data_filter else collection.count_documents({})

    @operation
    def __get_collection_datas(self, collection: Collection, data_filter: Optional[dict] = None,
                               field: Optional[str] = '_id',
                               order: Optional[bool] = ASCENDING) -> Union[List[dict], dict]:
        """
        Retorna os dados da collection especificada.\n

        :param collection: collection onde os dados serão retornados.
        :param data_filter: dado a ser filtrado.
        :param field: forma que o dado será ordenado.
        :param order: boolean para identificar se os dados virão na ordem crescente ou descrescente.
        :return: dados da collection.
        """

        return collection.find_one(data_filter) if data_filter else list(collection.find({}).sort(field, order))

    @void_operation
    def insert(self, data: [List[dict], dict], collection: Collection) -> None:
        """
        Insersão de novos dados.

        :param collection: collection onde os dados serão inseridos.
        :param data: dados a serem inseridos.
        """

        collection.insert_many(data) if type(data) == list else collection.insert_one(data)

    @void_operation
    def update_datas(self, new_datas: List[dict], collection: Collection) -> None:
        """
        Atualização de dados de uma determinada collection.\n

        :param collection: collection onde os dados serão atualizados.
        :param new_datas: dados a serem inseridos.
        """

        collection_datas: List[dict] = remove_element(
            self.__get_collection_datas(collection, field='delegacia'), '_id')

        to_update: List[dict] = [new_datas[value] for value in range(len(collection_datas)) if
                                 new_datas[value] != collection_datas[value]]

        old_datas: List[dict] = [collection_datas[value] for value in range(len(collection_datas)) if
                                 collection_datas[value] != new_datas[value]]

        if len(to_update) != 0:
            info(f'Iniciando atualização de {len(to_update)} dado(s) na collection {collection.name}.')

            for value in range(len(to_update)): collection.update_one(old_datas[value], {'$set': to_update[value]})
            info("Dados atualizados com sucesso.")
        else:
            info(f'Não há dados a serem atualizados.')

        if len(new_datas) != len(collection_datas):
            to_insert: List[dict] = []
            info(f'Encontrado {len(new_datas) - len(collection_datas)} novo(s) dado(s) obtido durante o scraping.')

            for value in range(len(new_datas)):
                datas: dict = self.__get_collection_datas(collection, {'delegacia': new_datas[value]['delegacia']})

                if datas is None:
                    to_insert.append(new_datas[value])
            self.insert(to_insert, collection)

            info(f'{len(new_datas) - len(collection_datas)} novo(s) dado(s) inserido na collection {collection.name}.')
