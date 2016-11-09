from repository.mongo_repository import *
from abc import ABCMeta


class FaturamentoRepository(GenericRepository):
    __metaclass__ = ABCMeta


class FaturamentoRepositoryMongo(FaturamentoRepository, GenericMongoRepository):
    def __init__(self, repository, collection_name):
        # inject the collection name
        self.repository = repository
        self.repository.collection_name = collection_name
