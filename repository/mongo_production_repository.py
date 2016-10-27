from repository_factory import RepositoryFactory
from pymongo import MongoClient
from mongo_client_singleton import MongoClientSingleton


class MongoProductionRepository(RepositoryFactory):
    def __init__(self, args):
        super(RepositoryFactory)
        self.args = args

    def get_data_source(self):
        client = MongoClientSingleton.build_mongo_client(self.args.mongo_database_url)
        return client[self.args.mongo_database_name]