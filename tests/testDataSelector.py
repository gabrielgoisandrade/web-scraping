import unittest
from functools import wraps
from time import sleep, time
from typing import List, Union, Optional

from bs4 import BeautifulSoup
from pymongo.errors import PyMongoError
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

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
        Select(driver.find_element_by_name(__region)).select_by_value('1')
        Select(driver.find_element_by_name(__police_station)).select_by_value('1410')
        driver.find_element_by_id(__button).click()
        sleep(1.5)
        td = list(map(lambda x: x.text, BeautifulSoup(driver.find_element_by_id(__table)
                                                      .get_attribute('innerHTML'), 'html.parser').select('td')))

        print(td[196: 196 + 14])

    def test_outro(self):
        current_datas: List[dict] = [{
            "nome": 'Gabriel',
            'idade': 20
        }, {
            "nome": 'Gabriel',
            'idade': 21
        }, {
            "nome": 'Gabriel',
            'idade': 22
        }, {
            "nome": 'Gabriel',
            'idade': 23
        }]

        scraping_datas: List[dict] = [{
            "nome": 'Gabriel',
            'idade': 20
        }, {
            "nome": 'Gabriel',
            'idade': 29
        }, {
            "nome": 'Gabriel',
            'idade': 42
        }, {
            "nome": 'Gabriel',
            'idade': 53
        }]

        # _old = list(filter(lambda old: old != scraping_datas, current_datas))
        # print(_old)
        # _new = list(filter(lambda new: new != current_datas, scraping_datas))
        # print(_new)
        # operations.insert(current_datas)
        # operations.update_datas(list(filter(lambda old: old != scraping_datas, current_datas)),
        #                         list(filter(lambda new: new != current_datas, scraping_datas)))

        a = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Total']

        def teste_lambda():
            inicio = time()
            print(list(map(lambda x: x.lower(), filter(lambda y: y != 'Total', a))))
            fim = time()
            print(fim - inicio)

        def teste_for():
            inicio = time()
            print([x.lower() for x in a if x != 'Total'])
            fim = time()
            print(fim - inicio)

        teste_for()
        print('============================')
        teste_lambda()

        # for x in range(len(scraping_datas)):
        #     a = scraping_datas[x]
        #     b = current_datas[x]
        #     print(list(filter(lambda y: y != a, b.items())))

        if __name__ == '__main__': unittest.main()
