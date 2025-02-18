from AbstractModule import AbstractModule
from MessageBus import MessageBus
import random


class ExampleModule(AbstractModule):

    def prep(self, register_cmd_callback):
        """
        register command
        :return:
        """

        register_cmd_callback("dosth", self.cmd_example)
        pass

    def cmd_example(self, args):
        print(f"command example: {args}")

    def update(self, dtime: float, bus: MessageBus):


        for m in bus.iterate_messages():
            info = m.get_info()
            if info["type"] == "svg_cashtype_data":
                # print(f"content: {info["content"]}")
                m.set_checked()

        pass

    def quit(self):
        pass

    def __init__(self, bus: MessageBus):
        super().__init__(bus)

