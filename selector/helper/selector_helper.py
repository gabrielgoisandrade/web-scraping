from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select


class SelectorHelper:

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def get_values(self, name: str) -> dict:
        """
        Pega os dados de determinado select option.

        :param name: name do select.
        :return: dict contendo as opções e seus valores correspondentes.
        """

        select = Select(self.__driver.find_element_by_name(name)).options

        key: list = [option.text for option in select]

        value: list = [option.get_attribute('value') for option in select]

        return {key[option]: value[option] for option in range(len(key))}

    def select_option(self, name: str, value) -> None:
        """
        Seleciona um determinado valor dentro do select option.

        :param name: name do select.
        :param value: valor a ser selecionado.
        """

        selected_option = Select(self.__driver.find_element_by_name(name))

        selected_option.select_by_value(str(value))

    def get_raw_table(self, id_table: str) -> list:
        """
        Pega o código HTML da tabela, com os registros que são gerados a cada vez que uma delegacia é
        selecionada.

        :param id_table: id da tabela.
        :return: list com a tabela (código HTML).
        """

        return self.__driver.find_element_by_id(id_table).get_attribute('innerHTML')

    def filter_police_stations(self, name: str) -> dict:
        """
        Remove delegacias que não serão usadas durante o scraping.

        :param name: name do select option.
        :return: dict com apenas as delegacias que serão usadas durante o scraping.
        """

        select_values = self.get_values(name)

        return {key: value for key, value in select_values.items()
                if 'DP' in key
                and 'Central de Flagrantes II' not in key
                and 'Pessoa com Deficiência' not in key}
