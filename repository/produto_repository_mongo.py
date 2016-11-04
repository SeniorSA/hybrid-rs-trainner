from abc import abstractmethod, ABCMeta
from repository.repository_factory import RepositoryFactory
from repository.produto_repository import ProdutoRepository
from repository.mongo_repository import GenericMongoRepository

class ProdutoRepositoryMongo(ProdutoRepository, GenericMongoRepository):
    def __init__(self, repository):
        self.repository = repository

    def get_items_code(self):
        db = self.repository.get_data_source()
        item_colls = db[self.repository.args.item_collection_name]
        customer_codes = item_colls.distinct('codigo')

        return customer_codes