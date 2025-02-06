from AbstractModule import AbstractModule
from MessageBus import MessageBus


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
        print(f"I am a module {dtime}")
        pass

    def quit(self):
        pass

    def __init__(self):
        super().__init__()

