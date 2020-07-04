from logging import basicConfig, error, INFO, info, critical
from os.path import join


class LogConfig:

    def __init__(self, msg: str):
        basicConfig(filename='app.log', filemode='w+',
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=INFO)
        self.__msg = msg

    def log_error(self) -> None: error(self.__msg)

    def log_info(self) -> None: info(self.__msg)

    def log_critical(self) -> None: critical(self.__msg)
