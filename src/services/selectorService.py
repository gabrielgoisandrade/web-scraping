from datetime import datetime
from os.path import join
from time import sleep
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from src.database import operations
from src.selector.helper.selectorHelper import SelectorHelper


class SelectorService:

    def __init__(self):
        options = Options()
        options.headless = True
        self.__driver: WebDriver = Chrome(executable_path=join('utils/driver', 'chromedriver.exe'), options=options)
        self.__helper = SelectorHelper(self.__driver)

    def open_browser(self, url: str) -> None:
        """
        Abre o navegador na url passada.

        :param url: endereço web do site a ser aberto.
        """

        self.__driver.get(url)

    def click_button(self, _id: str) -> None:
        """
        Clica no botão que contém o id passado.

        :param _id: id do botão a ser clicado.
        """

        sleep(1.5)
        self.__driver.find_element_by_id(_id).click()

    def select_year(self, name: str, value: int) -> None:
        """
        Seleciona um ano do select option.

        :param name: name do select option.
        :param value: ano a ser selecionado.
        """

        sleep(1.5)
        self.__helper.select_option(name, value)

    def select_region(self, name: str, value: str) -> None:
        """
        Seleciona uma região do select option.

        :param name: name do select option.
        :param value: região a ser selecionada.
        """

        sleep(1.5)
        select_value = self.__helper.get_values(name)[value]
        self.__helper.select_option(name, select_value)

    def select_city(self, name: str, value: str) -> None:
        """
        Seleciona uma cidade do select option.

        :param name: name do select option.
        :param value: cidade a ser selecionada.
        """

        sleep(1.5)
        select_value = self.__helper.get_values(name)[value]

        self.__helper.select_option(name, select_value)

    def select_police_stations(self, year, name: str, id_table: str) -> None:
        """
        Seleciona as delegacias e prepara os dados capturados para serem inseridos no banco de dados.

        :param year: ano da ocorrência.
        :param name: name do select option.
        :param id_table: id da tabela.
        """

        from src.services import extractor

        scraping_datas: List[dict] = []

        filtered_police_station: dict = self.__helper.filter_police_stations(name)

        for police_station, option_value in filtered_police_station.items():
            sleep(1.5)
            self.__helper.select_option(name, option_value)

            raw_table: list = self.__helper.get_raw_table(id_table)

            records: dict = extractor.records(raw_table=raw_table, crime='ESTUPRO',
                                              police_station=police_station)

            scraping_datas.append(records)

        operations.insert(scraping_datas) if year == datetime.now().year - 1 \
            else operations.insert(scraping_datas, True)
