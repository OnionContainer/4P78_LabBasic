from abc import ABC, abstractmethod
from typing import List

from MessageBus import MessageBus


class AbstractModule(ABC):

    def __init__(self, bus:MessageBus):
        self.__bus = bus
        pass

    def _push_message(self, msg):
        self.__bus.push_message(self, msg)

    def _peek_message(self, key, auto_check=True)->None|List[dict]:
        """
        Change Reminder: if you see and bug about this interface, we changed from return one thing to return everything
        :param key: the type of message you look for
        :return: the message content
        """
        result = []
        for msg in self.__bus.iterate_messages():
            info = msg.get_info()
            if info["type"] == key:
                if auto_check:
                    msg.set_checked()
                result.append(info)
                # return info
        if len(result) == 0:
            return None
        return result

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
