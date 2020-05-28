from datetime import datetime
from time import sleep
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from database import get_collection_datas, current_year_occurrences, last_year_occurrences
from selector.helper.selector_helper import SelectorHelper


class SelectorService:

    def __init__(self):
        options = Options()
        options.headless = True
        self.__driver: WebDriver = Chrome(options=options)
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

        from services import extractor, send, update

        scraping_datas: List[dict] = []

        filtered_police_station: dict = self.__helper.filter_police_stations(name)

        for police_station, option_value in filtered_police_station.items():
            sleep(1.5)
            self.__helper.select_option(name, option_value)

            scraping_datas.append(extractor.prepare_records(police_station, police_station.split('-')[1].strip(),
                                                            raw_table=self.__helper.get_raw_table(id_table=id_table)))

        if year == datetime.now().year - 1:
            if len(get_collection_datas(last_year_occurrences())) == 0:
                send.send_datas(last_year_occurrences(), scraping_datas)
            else:
                update.update_occurrences(last_year_occurrences(), scraping_datas)

        elif len(get_collection_datas(current_year_occurrences())) == 0:
            send.send_datas(current_year_occurrences(), scraping_datas)
        else:
            update.update_occurrences(current_year_occurrences(), scraping_datas)
