from abc import abstractmethod, ABCMeta


class CustomerRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_customers_code(self): pass
