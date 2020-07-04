from src.log import info
from ..services.selectorService import SelectorService


class DataSelector:
    __selector = SelectorService()

    def __init__(self, years: list): self.__years = years

    def select_datas(self):
        """
        Método responsável por interagir com todos os filtros e elementos do site, fazendo com que os dados
        a serem extraídos fiquem acessíveis.
        """

        self.__selector.open_browser()

        self.__selector.click_button()

        for year in self.__years:
            info(f'Selecionando o ano {year}.')
            self.__selector.select_year(value=str(year))

            info('Selecionando a região.')
            self.__selector.select_region(value='Capital')

            info('Selecionando o município.')
            self.__selector.select_city(value='São Paulo')

            info('Selecionando as delegacias.')
            self.__selector.select_police_stations(year=year)
