from datetime import datetime
from time import sleep

from log import info
from selector.dataSelector import DataSelector

if __name__ == '__main__':
    current_year: int = datetime.now().year
    last_year: int = datetime.now().year - 1

    info('Aplicação iniciada.')

    while True:
        info(f'Inciando coleta de dados de {current_year} e {last_year}.')
        DataSelector([current_year, last_year]).select_datas()

        info('Aplicação finalizada. Aguardando nova retomada.')
        sleep(24 * 3600)
