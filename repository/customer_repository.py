from abc import abstractmethod, ABCMeta


class CustomerRepository():
    @abstractmethod
    def get_customers_code(self): pass

    @abstractmethod
    def add_customer(self, customer): pass

    @abstractmethod
    def count(self): pass
