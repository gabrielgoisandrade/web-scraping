from json import dump
from os.path import join
from typing import List


class WriteFileService:

    @staticmethod
    def write_csv():
        pass

    @staticmethod
    def write_txt():
        pass

    @staticmethod
    def write_json(file_name: str, data: List[dict]) -> None:
        """
        Cria um arquivo JSON com os dados de determinada collection.

        :param file_name: nome do arquivo
        :param data: dados a serem escritos.
        """

        with open(join('./', f'{file_name}.json'), 'w', encoding='UTF-8') as _json:
            dump(obj=data, fp=_json, ensure_ascii=False, indent=4)
