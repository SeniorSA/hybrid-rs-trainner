from abc import abstractmethod, ABCMeta
from repository.repository_factory import RepositoryFactory
from repository.customer_repository import CustomerRepository


class CustomerRepositoryMongo(CustomerRepository):
    def __init__(self, repository):
        self.repository = repository

    def get_customers_code(self):
        db = self.repository.get_data_source()
        customer_colls = db[self.repository.args.customer_collection_name]
        customer_codes = customer_colls.distinct('codigo')

        return customer_codes

    def add_customer(self, customer):
        db = self.repository.get_data_source()[self.repository.args.mongo_database_name]
        db[self.repository.args.customer_collection_name].save(customer)

    def count(self):
        db = self.repository.get_data_source()[self.repository.args.customer_collection_name]
        return db.count()