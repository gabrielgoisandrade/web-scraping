from typing import List, Optional

from pymongo.collection import Collection

from src import info
from src.database.operationsDatabase import OperationsDatabase


class SendDataService:
    __operations = OperationsDatabase()

    @classmethod
    def verify_datas(cls, scraping_datas: List[dict], is_current_occurrences: Optional[bool] = False) -> None:
        """
        Verifica a necessidade de insersão, ou atualização dos dados já existentes.\n

        :param scraping_datas: dados obtidos durante o scraping.
        :param is_current_occurrences: boolean usado para identificar em qual collection os daodos serão inseridos,
                ou atualizados
        """

        coll: Collection = cls.__operations.collection(is_current_occurrences)

        if cls.__operations.count_documents(coll) == 0:
            info(f'Insersão de {len(scraping_datas)} novo(s) dado(s) na collection '
                 f'{"current_occurrences" if is_current_occurrences else "last_occurrences"}.')

            cls.__operations.insert(scraping_datas, coll)
        else:
            cls.__operations.update_datas(scraping_datas, coll)
