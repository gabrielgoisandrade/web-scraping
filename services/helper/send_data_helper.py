from statistics import mean
from typing import List

from pymongo.collection import Collection

from database import remove_element, get_collection_datas


class SendDataHelper:

    def prepare_data_to_hdiyc(self, regions: list, **collections: Collection) -> List[dict]:
        """
        Prepara e retorna os dados no formato da collection hdiyc.

        :param regions: regiões.
        :param collections: kwargs contendo as collections necessárias para realizar as consultas.
        :return: dados já preparados.
        """

        datas: List[dict] = []
        for region in regions:
            datas.append({
                'regiao': region,
                'registros': self.__records_and_total(collections['current'], str(region)),
                'comparativo': {
                    'ano_atual': {
                        'media_anual': f"""{mean(self.__records(collections['current'], str(region))
                                                          .values()): 0.2f}""",
                    },
                    'ano_passado': {
                        'media_anual': f"""{mean(self.__records(collections['last'], str(region))
                                                          .values()): 0.2f}""",
                    }
                }
            })

        return datas

    @staticmethod
    def __records_and_total(collection: Collection, region: str) -> dict:
        """
        Retorna os registros e o total das ocorrências de cada região.

        :param collection: collection a ser consultada.
        :param region: região usada como filtro.
        :return: registros da região que não estão como 0.
        """
        return {key: value for key, value
                in remove_element(get_collection_datas(collection, {'regiao': region}),
                                  '_id')['registros'].items()}

    @staticmethod
    def __records(collection: Collection, region: str) -> dict:
        """
        Retorna os registros das ocorrências de cada região.

        :param collection: collection a ser consultada.
        :param region: região usada como filtro.
        :return: registros da região.
        """
        return {key: value for key, value
                in remove_element(get_collection_datas(collection, {'regiao': region}),
                                  '_id')['registros'].items() if key != 'Total'}
