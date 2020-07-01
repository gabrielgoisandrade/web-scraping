from bs4 import BeautifulSoup

from src.log import error, info


class ExtractorService:

    def records(self, raw_table: list, crime: str, police_station: str) -> dict:
        """
        Gera um dict contendo as informações da delegacia, região e os registros de estupro.

        :param raw_table: código HTML coletado durante a seleção de dados.
        :param crime: crime usado como palavra chave, para obter os valores por mês.
        :param police_station: informação da delegacia e região aonde atua.
        :return: dict com as informações de delegacia e registros de estupro.
        """
        region: str = police_station.split('-')[1].strip()

        return {
            'delegacia': police_station,
            'regiao': region,
            'registros': self.__get_records(raw_table, crime, region)
        }

    @staticmethod
    def __extract_table_value(raw_table: list, table_tag: str) -> list:
        """
        Elimina o código HTML das partes da tabela, que contém determinada tag, deixando apenas os valores.

        :param raw_table: list contendo a tabela (código HTML) com os registros referentes a delegacia selecionada.
        :param table_tag: parte da tabela a ser tratada.
        :return: list com os valores tratados.
        """

        return list(map(lambda value: value.text, BeautifulSoup(raw_table, 'html.parser').select(table_tag)))

    def __get_records(self, raw_table: list, crime: str, region: str) -> dict:
        """
        Obtém os registros de determinado crime que esteja presente na tabela de ocorrências, trantando os dados \n
        e montando um dict com os valores obtidos. \n

        :param crime: crime usado como palavra chave, para obter os registros referentes ao mesmo.
        :param raw_table: list contendo a tabela (código HTML) com os registros referentes a delegacia selecionada.
        :raise ValueError: caso o crime passado não seja encontrado.
        :return: dict contendo os registros de cada mês e o total.
        """

        table_header: list = self.__extract_table_value(raw_table, 'th')
        table_datas: list = self.__extract_table_value(raw_table, 'td')

        try:
            key_word: int = table_datas.index(crime)
        except ValueError as e:
            error(f'Erro ao obter os dados da região {region}.\n Detalhes: {e.__str__()}')
            raise ValueError(f'O crime {crime} não está presente na tabela.')
        else:
            records: list = table_datas[key_word: key_word + len(table_header)]

            keys: list = list(map(lambda to_lower: to_lower.lower(),
                                  filter(lambda value: value != 'Natureza', table_header)))

            records.pop(0)
            values: list = list(map(lambda value: float(value.replace('...', '0')), records))

            info(f'Registros da região {region} obtidos.')

            return dict(zip(keys, values))
