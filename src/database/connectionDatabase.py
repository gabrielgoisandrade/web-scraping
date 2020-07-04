from pymongo import MongoClient
from pymongo.errors import (ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError)

from src.log import info, critical


class ConnectionDatabase:
    __PSSW: str = 'DX7cYLYxxw65gyN'
    __DATABASE: str = 'scraping'
    __CLUSTER: str = 'personal-projects'

    @classmethod
    def __connection(cls) -> MongoClient:
        """
        Conexão com o banco de dados na cloud.

        :return: client.
        :raise ConncectionFailure: problemas ao conectar.
        :raise ConfigurationError: erro na string de conexão.
        """

        try:
            connection: MongoClient = MongoClient(f'mongodb+srv://projects:{cls.__PSSW}@'
                                                  f'{cls.__CLUSTER}-5djcq.mongodb.net/{cls.__DATABASE}?'
                                                  f'retryWrites=true&w=majority')
            info('Connected!')
            return connection
        except ConnectionFailure as e:
            critical(f'Erro ao conectar no cluster: {str(e.args)}')
        except ConfigurationError as e:
            critical(f'Erro ao conectar no cluster: {str(e.args)}')
        except ServerSelectionTimeoutError as e:
            critical(f'Erro ao conectar no cluster: {str(e.args)}')
            raise ServerSelectionTimeoutError('Erro ao conectar no cluster')

    @property
    def get_connection(self):
        return self.__class__.__connection()
