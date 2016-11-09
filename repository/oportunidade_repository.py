from abc import abstractmethod, ABCMeta
from mongo_repository import *
from repository.mongo_repository import GenericMongoRepository


class OportunidadeRepository(GenericRepository):
    __metaclass__ = ABCMeta


class OportunidadeRepositoryMongo(OportunidadeRepository, GenericMongoRepository):
    def __init__(self, repository, collection_name):
        self.repository = repository
        self.repository.collection_name = collection_name
