from mongomock import MongoClient
from repository.repository_factory import RepositoryFactory


class MongoMockRepository(RepositoryFactory):
    def get_data_source(self):
        fake_connection = MongoClient()
        return fake_connection['test']
