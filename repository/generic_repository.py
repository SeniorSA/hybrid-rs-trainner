from abc import abstractmethod


class GenericRepository(object):
    @abstractmethod
    def count(self): pass

    @abstractmethod
    def find(self, skip, top): pass
