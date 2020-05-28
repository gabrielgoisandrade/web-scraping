from typing import List, Optional, Union

from pymongo.collection import Collection
from pymongo.errors import BulkWriteError

from log import info, critical
from .connection_database import ConnectionDb

conn = ConnectionDb().connection()

db = conn.get_database('HDIYC_db')


def current_year_occurrences() -> Collection:
    if 'current_year_occurrences' not in db.list_collection_names():
        db.create_collection('current_year_occurrences')
    return db.get_collection('current_year_occurrences')


def last_year_occurrences() -> Collection:
    if 'last_year_occurrences' not in db.list_collection_names():
        db.create_collection('last_year_occurrences')
    return db.get_collection('last_year_occurrences')


def hdiyc() -> Collection:
    if 'hdiyc' not in db.list_collection_names():
        db.create_collection('hdiyc')
    return db.get_collection('hdiyc')


def count_documents(collection: Collection, data_filter: Optional[dict] = None) -> int:
    """
    Retorna a quantidade de documents dentro de uma determinada collection.

    :param collection: collection a ser consultada.
    :param data_filter: dado a ser filtrado.
    :return: quantidad de documents.
    """

    if data_filter:
        return collection.count_documents(data_filter)
    return collection.count_documents({})


def get_collection_datas(collection: Collection, data_filter: Optional[dict] = None) -> Union[List[dict], dict]:
    """
    Retorna os dados de uma determinada collection.

    :param collection: collection a ser consultada.
    :param data_filter: dado a ser filtrado.
    :return: dados da collection.
    """

    if data_filter:
        return collection.find_one(data_filter)

    return [values for values in collection.find({})]


def send_new_datas(func):
    """
    Decorator para inserir novos dados numa collection.

    :param func: função a ser executada.
    :return: função interna
    """

    def insert(*args, **kwargs) -> None:
        coll: Collection = func(*args, **kwargs)[0]
        coll_datas: List[dict] = func(*args, **kwargs)[1]
        try:
            coll.insert_many(coll_datas)
            info('Dados salvos com sucesso.')
        except BulkWriteError as e:
            critical(f'Erro ao inserir dados. Detalhes: {e.details}')
        finally:
            conn.close()

    return insert


def update_datas(collection: Collection, old_datas: List[dict], new_datas: List[dict]) -> None:
    """
    Atualiza os dados de uma determinada collection.

    :param collection: collection a ser atualizada.
    :param old_datas: dados dados a serem atualizadods.
    :param new_datas: dados a serem inseridos.
    """

    try:
        [collection.update_one(old_datas[value], {'$set': new_datas[value]})
         for value in range(len(new_datas))]
        info('Dados atualizados com sucesso.')
    except BulkWriteError as e:
        critical(f'Erro ao atualizar dados. Detalhes: {e.details}')
    finally:
        conn.close()


def remove_element(data: [List[dict], dict], to_remove: str) -> Union[List[dict], dict]:
    """
    Remove um elemento de um list.

    :param data: dados contendo esse elemento.
    :param to_remove: elemento a ser removido.
    :return: dados sem o elemento especificado.
    """

    if type(data) is list:
        processed_datas: List[dict] = []
        for value in data:
            value.pop(to_remove)
            processed_datas.append(value)
        return processed_datas
    return {key: value for key, value in data.items() if key != '_id'}
