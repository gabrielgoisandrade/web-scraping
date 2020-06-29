from bs4 import BeautifulSoup
from unidecode import unidecode

from log import info, critical


class ExtractorService:

    def prepare_records(self, police_station: str, region: str, raw_table: list) -> dict:
        """
        Gera um dict contendo as informações da delegacia, região e os registros de estupro.

        :param police_station: informação da delegacia.
        :param region: região da delegacia
        :param raw_table: list contendo a tabela (código HTML) com os registros referentes a delegacia selecionada.
        :return: dict com as informações de delegacia e registros de estupro.
        """

        headers_as_keys: list = [header.lower() for header in self.convert_table(raw_table, 'th')
                                 if header != 'Natureza']

        values: list = self.get_monthly_occurrences(raw_table)

        return {
            'delegacia': police_station,
            'regiao': unidecode(region.lower()),
            'registros': {headers_as_keys[value]: values[value] for value in range(len(values))}
        }

    @staticmethod
    def convert_table(raw_table: list, table_tag: str) -> list:
        """
        Elimina o código HTML das partes da tabela, que contém determinada tag, deixando apenas os valores.

        :param raw_table: list contendo a tabela (código HTML) com os registros referentes a delegacia selecionada.
        :param table_tag: parte da tabela a ser tratada.
        :return: list com os valores tratados.
        """

        return [value.text for value in BeautifulSoup(raw_table, 'html.parser').select(table_tag)]

    def get_monthly_occurrences(self, raw_table: list) -> list:
        """
        Pega as ocorrências referentes a estupro, registradas em cada mês.

        :param raw_table: list contendo a tabela (código HTML) com os registros referentes a delegacia selecionada.
        :return: list com os registros de estupro registrados em cada mês, já convertidos para int.
        """

        try:
            record_index: int = self.convert_table(raw_table, 'td').index('ESTUPRO')

            table_datas: list = self.convert_table(raw_table, 'td')

            values = [table_datas[record_index + value] for value in range(14)
                      if table_datas[record_index + value] != 'ESTUPRO']

            for value in range(len(values)):
                if values[value] == '...': values[value] = 0

            return [int(value) for value in values]
        except IndexError as e:
            critical(f'Erro ao capturar os registros. Erro: {str(e.args)}')
            raise
        finally:
            info('Registros capturados.')
