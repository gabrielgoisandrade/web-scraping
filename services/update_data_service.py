from typing import List

from pymongo.collection import Collection

from database import (update_datas, get_collection_datas, remove_element, hdiyc, last_year_occurrences,
                      current_year_occurrences)
from log import info
from .helper import send_data_helper


class UpdateDataService:

    def update_occurrences(self, collection: Collection, scraping_datas: List[dict]) -> None:
        """
        Atualização dos dados existentes, pelos novos dados obtidos durante o scraping.

        :param collection: collection onde os dados serão inseridos.
        :param scraping_datas: dados pegos durante o scraping.
        """
        regions: list = [scraping_datas[region]['regiao'] for region in range(len(scraping_datas))]

        current_collection_datas: List[dict] = [remove_element(get_collection_datas(collection, {'regiao': region}),
                                                               '_id') for region in regions]

        new_datas: List[dict] = self.__new_datas(current_collection_datas, scraping_datas)

        old_datas: List[dict] = self.__old_datas(current_collection_datas, scraping_datas)

        if len(new_datas) == 0:
            info('Não há dados a serem atualizados.')
            return

        info('Iniciando atualização de dados.')
        update_datas(current_year_occurrences(), old_datas, new_datas)
        self.__update_hdiyc(new_datas)

    def __update_hdiyc(self, scraping_datas: List[dict]) -> None:
        """
        Atualiza os dados da colleciton principal.

        :param scraping_datas: novos dados obtidos durante o scraping.
        """

        info('Iniciando atualização dos dados da main collection.')

        regions: list = [scraping_datas[region]['regiao'] for region in range(len(scraping_datas))]

        current_collection_datas: List[dict] = [remove_element(get_collection_datas(hdiyc(), {'regiao': region}),
                                                               '_id') for region in regions]

        current_scraping_datas: List[dict] = send_data_helper \
            .prepare_data_to_hdiyc(regions, current=current_year_occurrences(), last=last_year_occurrences())

        new_datas: List[dict] = self.__new_datas(current_collection_datas, current_scraping_datas)

        old_datas: List[dict] = self.__old_datas(current_collection_datas, current_scraping_datas)

        update_datas(hdiyc(), old_datas, new_datas)

    @staticmethod
    def __new_datas(current_collection_datas: List[dict], current_scraping_datas: List[dict]) -> List[dict]:
        return [current_scraping_datas[value] for value in range(len(current_scraping_datas))
                if current_scraping_datas[value] != current_collection_datas[value]]

    @staticmethod
    def __old_datas(current_collection_datas: List[dict], current_scraping_datas: List[dict]) -> List[dict]:
        return [current_collection_datas[value] for value in range(len(current_collection_datas))
                if current_collection_datas[value] != current_scraping_datas[value]]
