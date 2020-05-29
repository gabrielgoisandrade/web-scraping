from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from log import error, info


class ConnectionDb:
    __USER: str = 'seu user'
    __PSSW: str = 'sua senha'
    __CLUSTER: str = 'seu cluster'
    __DATABASE: str = 'seu database'

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
