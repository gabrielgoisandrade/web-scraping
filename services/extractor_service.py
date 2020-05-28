from unidecode import unidecode

from services.helper import extractor_helper


class ExtractorService:

    @staticmethod
    def prepare_records(police_station: str, region: str, raw_table: list) -> dict:
        """
        Gera um dict contendo as informações da delegacia, região e os registros de estupro.

        :param police_station: informação da delegacia.
        :param region: região da delegacia
        :param raw_table: list contendo a tabela (código HTML) com os registros referentes a delegacia selecionada.
        :return: dict com as informações de delegacia e registros de estupro.
        """

        headers_as_keys: list = [header.lower() for header in extractor_helper.convert_table(raw_table, 'th')
                                 if header != 'Natureza']

        values: list = extractor_helper.get_monthly_occurrences(raw_table)

        return {
            'delegacia': police_station,
            'regiao': unidecode(region.lower()),
            'registros': {headers_as_keys[value]: values[value] for value in range(len(values))}
        }
