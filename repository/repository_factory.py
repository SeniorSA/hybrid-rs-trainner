from abc import abstractmethod, ABCMeta


class RepositoryFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data_source(self): pass
