from AbstractModule import AbstractModule
from ActualArm.ArmControl import ArmControl
from MessageBus import MessageBus, Message
from Logger.Logger import Logger, LogLevel


class TestModule(AbstractModule):

    def __init__(self, bus: MessageBus):
        super().__init__(bus)

    def msg_on_real_draw_time(self, message:Message):
        pass

    def prep(self, register_cmd_callback):
        print("Test Module")
        a = Logger.i().read_hot_argument("_example")
        print(a)
        print(type(a))
        print(set(a))

        def on_press():
            print(Logger.i().read_hot_argument("_example"))
            pass

        register_cmd_callback("hot", on_press)


        pass

    def update(self, dtime: float):
        pass

    def quit(self):
        pass
