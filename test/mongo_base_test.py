import json
import unittest
from abc import ABCMeta
from argparse import Namespace

from repository.mongo_mock_repository import MongoMockRepository


class MongoDatabaseTest(unittest.TestCase):
    # __metaclass__ = ABCMeta
    """Class with setup and tearsdown for all others tests"""

    def setUp(self):
        print '--------------------SETUP----------------------'
        mock_args = self.mock_args()
        self.repository_mock = MongoMockRepository(mock_args)
        self.data_source = self.repository_mock.get_data_source()
        print self.data_source

        files_names = ['clientes-test.json', 'produtos-test.json', 'faturamentos-test.json']

        for file_name in files_names:
            collection_name = file_name.split('-')[0]
            with open('data\\' + file_name, 'r') as file:
                for line in file:
                    document = json.loads(line)
                    del document['_id']
                    self.data_source[collection_name].save(document)

    def tearDown(self):
        files_names = ['clientes-test.json', 'produtos-test.json', 'faturamentos-test.json']
        for file in files_names:
            collection_name = file.split('-')[0]
            self.data_source[collection_name].drop()

    def mock_args(self):
        args = Namespace(mongo_database_url='localhost', mongo_database_name='test',
                         customer_collection_name='clientes', item_collection_name='produtos',
                         billing_collection_name='faturamentos', weighs='uniform', leaf_size=30,
                         p=2, n_neighbors=5, kfold=10, alg='brute', distance_metric='euclidean'
                         )
        return args
