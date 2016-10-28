from abc import abstractmethod
from repository.generic_repository import GenericRepository


class ProdutoRepository(GenericRepository):

    @abstractmethod
    def get_items_code(self):
        db = self.repository.get_data_source()
        customer_colls = db[self.repository.args.customer_collection_name]
        items_codes = customer_colls.distinct('codigo')

        return items_codes