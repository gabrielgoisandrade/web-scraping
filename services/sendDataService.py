# from typing import List, Optional
#
# from pymongo.errors import BulkWriteError
#
# from database import conn, current_occurrences, last_occurrences
# from log import critical, info
#
#
# class SendDataService:
#
#     @staticmethod
#     def send_datas(datas: List[dict], is_current: Optional[bool] = False) -> None:
#         """
#         Insersão de dados em determinada colleciton.
#
#         :param is_current: caso os dados sejam inseridos na collection current_year ou last_year
#         :param datas: dados a serem inseridos.
#         """
#
#         try:
#             current_occurrences().insert_many(datas) if is_current else last_occurrences().insert_many(datas)
#             info('Dados salvos com sucesso.')
#         except BulkWriteError as e:
#             critical(f'Erro ao inserir dados. Detalhes: {e.details}')
#         finally:
#             conn.get_connection.close()
