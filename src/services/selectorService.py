from datetime import datetime
from time import sleep
from typing import List

from src.services import (select_option, filter_police_stations, driver, select_police_stations)
from src.services.extractorService import ExtractorService
from src.services.sendDataService import SendDataService


class SelectorService:
    __url: str = 'http://www.seguranca.sp.gov.br/Estatistica/Pesquisa.aspx'
    __button: str = 'conteudo_btnMensal'
    __year: str = 'ctl00$conteudo$ddlAnos'
    __police_station: str = 'ctl00$conteudo$ddlDelegacias'
    __region: str = 'ctl00$conteudo$ddlRegioes'
    __city: str = 'ctl00$conteudo$ddlMunicipios'
    __table: str = 'conteudo_divMensal'

    @classmethod
    def open_browser(cls) -> None:
        """ Abre o navegador. """

        driver.get(cls.__url)

    @classmethod
    def click_button(cls) -> None:
        """ Clica no botão que contém o id passado. """

        sleep(1.5)
        driver.find_element_by_id(cls.__button).click()

    @classmethod
    def select_year(cls, value: str) -> None:
        """
        Seleciona um ano.

        :param value: ano a ser selecionado.
        """

        sleep(1.5)
        select_option(cls.__year, value)

    @classmethod
    def select_region(cls, value: str) -> None:
        """
        Seleciona uma região.

        :param value: região a ser selecionada.
        """

        sleep(1.5)
        select_option(cls.__region, value)

    @classmethod
    def select_city(cls, value: str) -> None:
        """
        Seleciona uma cidade.

        :param value: cidade a ser selecionada.
        """

        sleep(1.5)
        select_option(cls.__city, value)

    @classmethod
    def select_police_stations(cls, year: int) -> None:
        """
        Seleciona as delegacias e prepara os dados capturados para serem inseridos no banco de dados.

        :param year: ano da ocorrência.
        """
        scraping_datas: List[dict] = []
        filtered_values = filter_police_stations(cls.__police_station)

        for police_station in filtered_values.keys():
            sleep(1)
            select_police_stations(cls.__police_station, filtered_values[police_station])

            records: dict = ExtractorService(police_station, cls.__table, 'ESTUPRO').records()
            scraping_datas.append(records)

        SendDataService().verify_datas(scraping_datas) if year == datetime.now().year - 1 \
            else SendDataService().verify_datas(scraping_datas, True)
