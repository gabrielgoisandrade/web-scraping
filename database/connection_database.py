from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from log import error, info


class ConnectionDb:
    __USER: str = 'hdiyc_db'
    __PSSW: str = 'USMTbkX8TfppIAdb'
    __CLUSTER: str = 'hdiyccluster'
    __DATABASE: str = 'HDIYC_db'

    @classmethod
    def connection(cls) -> MongoClient:
        """
        Conexão com o banco de dados na cloud.

        :return: client de conexão.
        :raise ConncectionFailure: problemas ao conectar.
        """

        try:
            connection: MongoClient = MongoClient(f'mongodb+srv://{cls.__USER}:{cls.__PSSW}@{cls.__CLUSTER}'
                                                  f'-9xxtn.azure.mongodb.net/{cls.__DATABASE}'
                                                  f'?retryWrites=true&w=majority')
            info('Connected!')
            return connection
        except ConnectionFailure as e:
            error(str(e.args))
