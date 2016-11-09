from mongomock import MongoClient
from repository.repository_factory import RepositoryFactory


class MongoMockRepository(RepositoryFactory):
    __data_source  = None

    def get_data_source(self):
        if MongoMockRepository.__data_source == None:
            MongoMockRepository.__data_source = MongoClient()

        return MongoMockRepository.__data_source[self.args.mongo_database_name]

    def __init__(self, args):
        self.args = args
