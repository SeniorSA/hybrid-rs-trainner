from abc import abstractmethod, ABCMeta


class CustomerRepository():
    @abstractmethod
    def get_customers_code(self): pass
