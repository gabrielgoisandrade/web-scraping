from typing import List, Tuple

from pymongo.collection import Collection

from database import (get_collection_datas, current_year_occurrences, count_documents, send_new_datas, remove_element,
                      last_year_occurrences, hdiyc)
from .helper import send_data_helper


class SendDataService:

    @staticmethod
    @send_new_datas
    def send_datas(collection: Collection, datas: List[dict]) -> Tuple[Collection, List[dict]]:
        """
        Insersão de dados em determinada colleciton.

        :param collection: collection onde os dados serão inseridos.
        :param datas: dados a serem inseridos.
        :return: tupla contendo a collection e os dados.
        """
        return collection, datas

    @staticmethod
    @send_new_datas
    def send_hdiyc_datas() -> Tuple[Collection, List[dict]]:
        """
        Insersão de novos dados na collection hdiyc

        :return: collection e os dados a serem inseridos.
        """

        regions: List[dict] = [remove_element(get_collection_datas(current_year_occurrences()), '_id')
                               [region]['regiao'] for region in range(count_documents(current_year_occurrences()))]

        return hdiyc(), send_data_helper.prepare_data_to_hdiyc(regions, current=current_year_occurrences(),
                                                               last=last_year_occurrences())
