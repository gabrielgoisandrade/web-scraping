import unittest
from tests import scraping_datas, current
from pymongo import MongoClient, ReturnDocument


class MyTestCase(unittest.TestCase):
    # def test_outro(self):
    #     connection: MongoClient = MongoClient('mongodb+srv://projects:DX7cYLYxxw65gyN@'
    #                                           'personal-projects-5djcq.mongodb.net/scraping?'
    #                                           'retryWrites=true&w=majority')
    #
    #     # self.assertIsNone(connection.get_database('scraping').get_collection('current_occurrences').find_one_and_update(
    #     #     {'regiao': 'Se'},
    #     #     {'$set': {'registros': {"jan": 2, "fev": 2, "mar": 1, "abr": 1, "mai": 0,
    #     #                             "jun": 0, "jul": 0, "ago": 0, "set": 0, "out": 0,
    #     #                             "nov": 0, "dez": 0, "total": 5}}},
    #     #     return_document=ReturnDocument.AFTER))
    #
    #     datas = [{'regiao': 'Sé', 'delegacia': 'aaa', 'registros': {}},
    #              {'regiao': 'Se', 'delegacia': 'aaa', 'registros': {}}]
    #
    #     for i in range(len(datas)):
    #         dt = connection.get_database('scraping').get_collection('current_occurrences').find_one_and_update(
    #             {'regiao': datas[i]['regiao']},
    #             {'$set': {'registros': {"jan": 2, "fev": 2, "mar": 1, "abr": 1, "mai": 0,
    #                                     "jun": 0, "jul": 0, "ago": 0, "set": 0, "out": 0,
    #                                     "nov": 0, "dez": 0, "total": 5}}},
    #             return_document=ReturnDocument.AFTER)
    #         # dt = connection.get_database('scraping').get_collection('current_occurrences') \
    #         #     .find_one({'regiao': datas[i]['regiao']})
    #         if dt is None:
    #             print(datas[i])
    #             # insert


    def test_outro2(self):

        new = [scraping_datas[x] for x in range(len(current)) if scraping_datas[x] != current[x]]
        print(new)

        # for value in range(len(current)):
        #     if scraping_datas[value] == current[value]:
        #         index = scraping_datas.index(scraping_datas[value])
        #         scraping_datas.pop(index)

        # print(scraping_datas)
