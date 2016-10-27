from abc import abstractmethod


class RepositoryFactory(object):
    @abstractmethod
    def get_data_source(self): pass