from AbstractModule import AbstractModule
from ActualArm.ArmControl import ArmControl
from MessageBus import MessageBus, Message


class ArmControlModule(AbstractModule):

    def __init__(self, bus: MessageBus):
        super().__init__(bus)
        self.__control = None
        self.__total_wait_time = 0.0
        self.__req_wait_time = 0.2
        self.__order_queue = None

    def msg_on_real_draw_time(self, message:Message):
        self.__total_wait_time = 0
        self.__order_queue = message.get_info()["content"]
        message.set_checked()

    def prep(self, register_cmd_callback):
        self.__control = ArmControl()
        pass



    def update(self, dtime: float, bus: MessageBus):

        for line in bus.iterate_messages():
            info = line.get_info()
            if info["type"] == "real_draw_time":
                self.msg_on_real_draw_time(line)
                bus.push_message(self, {
                    "type": "actuator_report",
                    "is_start": True
                })

        self.__total_wait_time += dtime
        if self.__total_wait_time > self.__req_wait_time:
            self.__total_wait_time = 0
            if self.__order_queue is not None and len(self.__order_queue) > 0:
                order = self.__order_queue.pop(0)
                filtered_order = (order[0], order[1] * -1 + 90, order[2])
                print(f"process_order {filtered_order}, remaining{len(self.__order_queue)}")
                self.__control.process_order(filtered_order)
                if len(self.__order_queue) == 0:
                    self._push_message({
                        "type": "actuator_report",
                        "is_start": False
                    })

    def quit(self):
        pass
