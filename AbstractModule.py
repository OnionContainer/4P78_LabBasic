from abc import ABC, abstractmethod

from MessageBus import MessageBus


class AbstractModule(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def prep(self):
        pass

    @abstractmethod
    def update(self, dtime:float, bus:MessageBus):
        """
        :param dtime: delta time(second)
        :param bus: message created by other module
        """
        pass

    @abstractmethod
    def quit(self):
        pass