from abc import abstractmethod

from AbstractModule import AbstractModule
from MessageBus import MessageBus


class EventModule(AbstractModule):

    def on(self, message_key):
        pass

    def emit(self, message_key, info):
        """

        :param message_key: string, message key
        :param info: dict
        :return:
        """

        pass

    @abstractmethod
    def prep(self, register_cmd_callback):
        pass
    @abstractmethod
    def update(self, dtime: float, bus: MessageBus):
        pass
    @abstractmethod
    def quit(self):
        pass

    def __init__(self, bus:MessageBus):
        super().__init__()
        self.__bus = bus