from abc import abstractmethod
from repository.generic_repository import GenericRepository
from repository.mongo_repository import GenericMongoRepository

class ProdutoRepository(GenericRepository):
    @abstractmethod
    def get_items_code(self): pass

class ProdutoRepositoryMongo(ProdutoRepository, GenericMongoRepository):
    def __init__(self, repository, collection_name):
        self.repository = repository
        self.repository.collection_name = collection_name

    def get_items_code(self):
        db = self.repository.get_data_source()
        item_colls = db[self.repository.args.item_collection_name]
        customer_codes = item_colls.distinct('codigo')

        return customer_codes