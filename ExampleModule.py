from AbstractModule import AbstractModule
from MessageBus import MessageBus


class ExampleModule(AbstractModule):

    def prep(self):
        """
        register command
        not done yet
        :return:
        """
        pass

    def update(self, dtime: float, bus: MessageBus):
        print(f"I am a module {dtime}")
        pass

    def quit(self):
        pass

    def __init__(self):
        super().__init__()

