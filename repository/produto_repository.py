from abc import abstractmethod
from repository.generic_repository import GenericRepository


class ProdutoRepository(GenericRepository):
    @abstractmethod
    def get_items_code(self): pass
