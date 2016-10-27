from pymongo import MongoClient


class MongoClientSingleton(object):
    __mongo_client = None

    @staticmethod
    def build_mongo_client(database_url='localhost'):
        if MongoClientSingleton.__mongo_client == None:
            MongoClientSingleton.__mongo_client = MongoClient(database_url)

        return MongoClientSingleton.__mongo_client
