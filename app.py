from datetime import datetime

from src import (DataSelector, info)

if __name__ == '__main__':
    current_year: int = datetime.now().year
    last_year: int = datetime.now().year - 1

    info('Aplicação iniciada.')

    info(f'Inciando coleta de dados.')
    DataSelector([current_year, last_year]).select_datas()
