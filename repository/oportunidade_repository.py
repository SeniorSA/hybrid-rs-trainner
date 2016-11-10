from abc import abstractmethod, ABCMeta
from mongo_repository import *
from repository.mongo_repository import GenericMongoRepository


class OportunidadeRepository(GenericRepository):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_customers_code(self):pass


class OportunidadeRepositoryMongo(OportunidadeRepository, GenericMongoRepository):
    def __init__(self, repository, collection_name):
        self.repository = repository
        self.repository.collection_name = collection_name

    def get_customers_code(self):
        db = self.repository.get_data_source()[self.repository.args.opportunity_collection_name]
        return db.distinct('codigoCliente')