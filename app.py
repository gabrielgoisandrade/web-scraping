from datetime import datetime
from time import sleep

from database import count_documents, hdiyc
from log import info
from selector.data_selector import DataSelector
from services import send

if __name__ == '__main__':
    current_year: int = datetime.now().year
    last_year: int = datetime.now().year - 1

    info('Aplicação iniciada.')

    while True:

        info(f'Inciando coleta de dados de {current_year} e {last_year}.')
        DataSelector([current_year, last_year]).select_datas()

        if count_documents(hdiyc()) == 0:
            info('Iniciando insersão de dados na main collection.')
            send.send_hdiyc_datas()
        info('Aplicação finalizada. Aguardando nova retomada.')
        sleep(24 * 3600)
