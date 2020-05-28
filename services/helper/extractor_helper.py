from bs4 import BeautifulSoup

from log import critical, info


class ExtractorHelper:

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
