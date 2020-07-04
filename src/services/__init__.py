from os.path import join
from typing import Iterable

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from src.log import error

options: Options = Options()
options.headless = True
driver: WebDriver = Chrome(executable_path=join('driver', 'chromedriver.exe'), options=options)


def select_option(name: str, value: str) -> None:
    """
    Seleciona uma opção do select option, pelo seu valor.

    :param name: name do select.
    :param value: valor a ser selecionado.
    """

    to_select: str = get_values(name)[value]

    try:
        Select(driver.find_element_by_name(name)).select_by_value(str(to_select))
    except NoSuchElementException as e:
        error(e.__str__())
        raise NoSuchElementException(f'Não foi possível encontrar a opção com o valor {to_select}')


def get_values(name: str) -> dict:
    """
    Mapeia o select option pegando cada opção, valore e estruturando num dict.

    :param name: name do select.
    :return: dict contendo os valores mapeados.
    """

    select: Iterable = Select(driver.find_element_by_name(name)).options

    keys: list = list(filter(lambda option: option != 'Todos',
                             map(lambda option: option.text, select)))

    values: list = list(filter(lambda attr: attr != '0',
                               map(lambda attr: attr.get_attribute('value'), select)))

    return dict(zip(keys, values))


def filter_police_stations(name: str) -> dict:
    """
    Remove delegacias que não serão utilizadas.

    :param name: name do select option.
    :return: dict com apenas as delegacias que serão utilizadas.
    """

    return {key: value for key, value in get_values(name).items()
            if 'DP' in key
            and 'Central de Flagrantes II' not in key
            and 'Pessoa com Deficiência' not in key}


def extract_table_value(id_table: str, tag: str) -> list:
    """
    Elimina o código HTML das partes da tabela que contém determinada tag, deixando apenas os valores.

    :param id_table: id da tabela.
    :param tag: parte da tabela a ser tratada.
    :return: list com os valores tratados.
    """

    raw_table: list = driver.find_element_by_id(id_table).get_attribute('innerHTML')

    return list(map(lambda value: value.text, BeautifulSoup(raw_table, 'html.parser').select(tag)))
