from src.log import error, info
from src.services import extract_table_value


class ExtractorService:

    def __init__(self, police_station: str, id_table: str, crime: str):
        self.__police_station = police_station
        self.__id_table = id_table
        self.__crime = crime
        self.__region = police_station.split('-')[1].strip()

    def records(self) -> dict:
        """
        Monta um dict contendo as informações da delegacia, região e os registros de estupro.

        :return: dict com as informações.
        """

        return {
            'policeStation': self.__police_station,
            'region': self.__region,
            'records': self.__get_records()
        }

    def __get_records(self) -> dict:
        """
        Obtém os registros de determinado crime que esteja presente na tabela de ocorrências, trantando os dados \n
        e montando um dict com os valores obtidos. \n

        :raise ValueError: caso o crime passado não seja encontrado.
        :return: dict contendo os registros de cada mês e o total.
        """

        table_header: list = ['dummy', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
                              'dec', 'total']

        table_datas: list = extract_table_value(self.__id_table, 'td')

        try:
            key_word: int = table_datas.index(self.__crime)

        except ValueError as e:
            error(f'Erro ao obter os dados da região {self.__region}.\n Detalhes: {e.__str__()}')

            raise ValueError(f'O crime {self.__crime} não está presente na tabela.')

        else:
            records: list = table_datas[key_word: key_word + len(table_header)]

            keys: list = list(filter(lambda value: value != 'dummy', table_header))

            records.pop(0)

            values: list = list(
                map(lambda value: float(value.replace('...', '0')), records)
            )

            info(f'Registros da região {self.__region} obtidos.')

            return dict(zip(keys, values))
