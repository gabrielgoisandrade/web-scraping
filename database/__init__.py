from typing import List, Union

from .connectionDatabase import ConnectionDatabase
from .operationsDatabase import OperationsDatabase

operations: OperationsDatabase = OperationsDatabase()
conn = ConnectionDatabase().get_connection


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
