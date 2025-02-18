from abc import ABC, abstractmethod

from MessageBus import MessageBus


class AbstractModule(ABC):

    def __init__(self, bus:MessageBus):
        self.__bus = bus
        pass

    def _push_message(self, msg):
        self.__bus.push_message(self, msg)

    def _peek_message(self, key, auto_check=True)->None|dict:
        """
        :param key: the type of message you look for
        :return: the message content
        """
        for msg in self.__bus.iterate_messages():
            info = msg.get_info()
            if info["type"] == key:
                if auto_check:
                    msg.set_checked()
                return info
        return None

    @abstractmethod
    def prep(self, register_cmd_callback):
        pass

    @abstractmethod
    def update(self, dtime:float):
        """
        :param dtime: delta time(second)
        """
        pass

    @abstractmethod
    def quit(self):
        pass
