from abc import abstractmethod, ABCMeta
from repository.repository_factory import RepositoryFactory
from repository.cliente_repository import ClienteRepository
from repository.mongo_repository import GenericMongoRepository

class ClienteRepositoryMongo(ClienteRepository, GenericMongoRepository):
    def __init__(self, repository, collection_name):
        self.repository = repository
        self.repository.collection_name = collection_name

    def get_customers_code(self):
        db = self.repository.get_data_source()
        customer_colls = db[self.repository.args.customer_collection_name]
        customer_codes = customer_colls.distinct('codigo')

        return customer_codes