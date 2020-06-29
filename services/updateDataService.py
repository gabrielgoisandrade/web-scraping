from typing import List

from pymongo.collection import Collection

from database import (update_datas, get_collection, remove_element, current_occurrences)
from log import info


class UpdateDataService:

    def update_occurrences(self, collection: Collection, scraping_datas: List[dict]) -> None:
        """
        Atualização dos dados existentes, pelos novos dados obtidos durante o scraping.

        :param collection: collection onde os dados serão inseridos.
        :param scraping_datas: dados pegos durante o scraping.
        """
        regions: list = [scraping_datas[region]['regiao'] for region in range(len(scraping_datas))]

        current_collection_datas: List[dict] = [remove_element(get_collection(collection, {'regiao': region}),
                                                               '_id') for region in regions]

        new_datas: List[dict] = self.__new_datas(current_collection_datas, scraping_datas)

        old_datas: List[dict] = self.__old_datas(current_collection_datas, scraping_datas)

        if len(new_datas) == 0:
            info('Não há dados a serem atualizados.')
            return

        info('Iniciando atualização de dados.')
        update_datas(current_occurrences(), old_datas, new_datas)

