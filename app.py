from datetime import datetime
from time import sleep

from src import DataSelector
from src import info

if __name__ == '__main__':
    current_year: int = datetime.now().year
    last_year: int = datetime.now().year - 1

    info('Aplicação iniciada.')

    while True:
        info(f'Inciando coleta de dados.')
        DataSelector([current_year, last_year]).select_datas()

        info('Aplicação finalizada. Aguardando nova retomada.')
        sleep(24 * 3600)
