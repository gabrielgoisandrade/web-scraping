from log import info
from services import (selector)


class DataSelector:
    __url: str = 'http://www.seguranca.sp.gov.br/Estatistica/Pesquisa.aspx'
    __button: str = 'conteudo_btnMensal'
    __year: str = 'ctl00$conteudo$ddlAnos'
    __police_station: str = 'ctl00$conteudo$ddlDelegacias'
    __region: str = 'ctl00$conteudo$ddlRegioes'
    __city: str = 'ctl00$conteudo$ddlMunicipios'
    __table: str = 'conteudo_divMensal'

    def __init__(self, years: list):
        self.__years = years

    def select_datas(self):
        """ Método responsável por selecionar os dados necessários para realização do scraping"""

        selector.open_browser(self.__url)

        selector.click_button(self.__button)

        for year in self.__years:
            info('Selecionando o ano.')
            selector.select_year(name=self.__year, value=year)

            info('Selecionando a região.')
            selector.select_region(name=self.__region, value='Capital')

            info('Selecionando o município.')
            selector.select_city(name=self.__city, value='São Paulo')

            info('Selecionando as delegacias.')
            selector.select_police_stations(year=year, name=self.__police_station, id_table=self.__table)
