from abc import abstractmethod, ABCMeta
from repository.repository_factory import RepositoryFactory
from repository.customer_repository import CustomerRepository
from repository.mongo_repository import GenericMongoRepository

class CustomerRepositoryMongo(CustomerRepository, GenericMongoRepository):
    def __init__(self, repository):
        self.repository = repository

    def get_customers_code(self):
        db = self.repository.get_data_source()
        customer_colls = db[self.repository.args.customer_collection_name]
        customer_codes = customer_colls.distinct('codigo')

        return customer_codes