import unittest
from functools import wraps
from pprint import pprint
from time import sleep
from typing import List, Union, Optional

from pymongo.errors import PyMongoError
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from database import operations
from log import error


class DatabaseHelper:

    @staticmethod
    def a(f):
        @wraps(f)
        def inner(data: Union[List[dict], dict], is_current_occurrences: Optional[bool] = False):
            if type(data) is not list or type(data) is not dict:
                error('Erro durante a insersão. Os dados devem ser do tipo list ou dict.')
                raise TypeError('Os dados devem ser do tipo list ou dict.')

            try:
                f(data, is_current_occurrences)
                print('nice, cachorro')
            except PyMongoError as e:
                error(e.__str__())

        return inner


class MyTestCase(unittest.TestCase):
    def test_something(self):
        __url: str = 'http://www.seguranca.sp.gov.br/Estatistica/Pesquisa.aspx'
        __button: str = 'conteudo_btnMensal'
        __year: str = 'ctl00$conteudo$ddlAnos'
        __police_station: str = 'ctl00$conteudo$ddlDelegacias'
        __region: str = 'ctl00$conteudo$ddlRegioes'
        __city: str = 'ctl00$conteudo$ddlMunicipios'
        __table: str = 'conteudo_divMensal'
        options = Options()
        options.headless = True
        driver = Chrome('C:/Users/Gabriel/Desktop/web-scraping/driver/chromedriver.exe', options=options)
        driver.get(__url)
        Select(driver.find_element_by_name(__year)).select_by_value('2020')
        sleep(1.5)
        tabela = driver.find_element_by_id('conteudo_repAnos_divGrid_0').get_attribute('innerHTML')

    def test_outro(self):
        print(pprint(operations.get_collection_datas(True, {"regiao": "se"})))


if __name__ == '__main__':
    unittest.main()
