from abc import abstractmethod, ABCMeta
from generic_repository import GenericRepository


class ClienteRepository(GenericRepository):

    @abstractmethod
    def get_customers_code(self): pass
