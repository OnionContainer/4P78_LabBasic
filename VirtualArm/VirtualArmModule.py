from copy import deepcopy
from typing import List

from AbstractModule import AbstractModule
from MessageBus import MessageBus, Message
from VirtualArm.VirtualArms import VirtualArms
import sympy

"""
VirtualArmModule

functions:
    1.maintain a VisualArms instance
    2.tell outside to draw VisualArms
    3.handle message:
        a) create VisualArms instance(skip) and draw it
        b) generate rotation plan
            and display rotation plan
        c) when plan is confirmed, send decision to ActuatorModule
        
Messages & cmd:
    <-cmd   move to     segt                done
    <-cmd   create      arm                 skipped
    <-msg   generate    plan                done
    ->msg   decision    to ActuatorModule   done?
    <-cmd   set         set                 done
    <-msg   bulk set    bset                in progress...
"""
class VirtualArmModule(AbstractModule):
    def __init__(self, bus:MessageBus):
        super().__init__(bus)
        self.__arm = None
        #data from svg module
        self.__data_in:List[(int, int)|int]|None = None
        self.__last_target = None
        #manipulation data to actuator
        self.__data_out:List[(int, int, int)]|None = None
        self.__is_pen_down = False

        self.__bus_ref = bus

    def msg_decision(self, bus:MessageBus):
        self.__data_in = None
        print(f"output data:\n {self.__data_out}\n output data ends")

        actual_data_out = []
        last = None
        for line in self.__data_out:
            if last == line:
                continue
            else:
                last = line
                actual_data_out.append(line)

        bus.push_message(self, {
            "type": "real_draw_time",
            "content": deepcopy(actual_data_out)
        })
        print(f"send draw message for actuator:\n{actual_data_out}")
        self.__data_out = None
        self.__is_pen_down = False
        return

    def msg_on_bulk_set(self, m:Message):
        print("bulk set called")
        m.set_checked()
        pendown = False
        info = m.get_info()
        self.__data_out = []
        for line in info["content"]:
            if type(line) is tuple:
                # self.__arm.force_set(line[0], line[1])
                can_move = self.__arm.move_to_good(
                    line[0],
                    line[1],
                    immediately=True
                )
                if not can_move:
                    continue
                else:
                    self.__data_out.append((
                        self.__arm.get_motor_angle(0),
                        self.__arm.get_motor_angle(1),
                        2 if pendown else 1
                    ))
            else:
                pendown = True if line == 1 else False

        self.msg_decision(self.__bus_ref)


    def msg_on_generate_ready(self, bus:MessageBus):
        for m in bus.iterate_messages():
            info = m.get_info()
            if info["type"] == "generate_ready":
                self.__data_in = deepcopy(info["content"])
                print(f"input data:\n {self.__data_in}\n input data ends")
                # self.__data_in.insert(0, (0,0))
                m.set_checked()
                self.__data_out = []
                self.__is_pen_down = False
                break

    def cmd_segt(self, pos=("0", "0)")):

        try:
            pos = (float(pos[0]), float(pos[1]))
        except ValueError as e:
            print(f"ValueError: {e}")
            return

        self.__arm.move_to_with_segments(*pos)

        pass

    def cmd_set(self, pos=("0", "0")):
        try:
            pos = (int(pos[0]), int(pos[1]))
        except ValueError as e:
            print(f"ValueError: {e}")
            return
        self.__arm.force_set(*pos)
        m0 = self.__arm.get_motor_angle(0)
        m1 = self.__arm.get_motor_angle(1)
        print(f"visual set to {m0}, {m1}")
        m0a = int(m0)
        m1a = int(m1)
        print(f"actuator set to {m0a}, {m1a}")
        self.__bus_ref.push_message(self, {
            "type": "real_draw_time",
            "content": [
                (m0a, m1a, 1),
            ]
        })


    def msgout_render_my_arm(self, bus:MessageBus):
        if self.__arm is None:
            return

        p1 = self.__arm.solve_node_pos(0)
        p2 = self.__arm.solve_node_pos(1)
        p3 = self.__arm.solve_node_pos(2)

        a0 = self.__arm.solve_angle_final(0)
        a1 = self.__arm.solve_angle_final(1)

        range1:sympy.Interval = self.__arm.get_motor_interval(0)
        range2:sympy.Interval = self.__arm.get_motor_interval(1)

        bus.push_message(self, {
            "type": "render_my_arm",
            "limits": [
                {
                    "x":p1[0],
                    "y":p1[1],
                    "radius":self.__arm.get_bar_length(0),
                    "start_angle":range1.start,
                    "extent":range1.measure,
                    "outline_color":"#a1beff",
                    "width":1
                },
                {
                    "x":p2[0],
                    "y":p2[1],
                    "radius":self.__arm.get_bar_length(1),
                    "extent":range2.measure,
                    "start_angle":range2.start + a0,
                    "outline_color":"#a1beff",
                    "width":1
                }
            ],
            "points":[p1,p2,p3]
        })

    def prep(self, register_cmd_callback):
        register_cmd_callback("segt", self.cmd_segt)
        self.__arm = VirtualArms()
        register_cmd_callback("set", self.cmd_set)
        pass

    def update(self, dtime: float):

        bus = self.__bus_ref#temp solution

        for msg in bus.iterate_messages():
            info = msg.get_info()
            if info["type"] == "bulk_set":
                self.msg_on_bulk_set(msg)
                break

        is_arm_mission_empty = self.__arm.update(dtime)
        self.msgout_render_my_arm(bus)

        if self.__data_out is not None:
            self.__data_out.append((
                int(self.__arm.get_motor_angle(0)),
                int(self.__arm.get_motor_angle(1)),
                2 if self.__is_pen_down else 1
            ))
            pass

        self.msg_on_generate_ready(bus)
        if is_arm_mission_empty and self.__data_in is not None and len(self.__data_in) >= 0:
            # print(self.__arm.get_is_error())
            if self.__arm.get_is_error():
                print("arm error detected")
                self.__data_in = None
                self.__data_out = None
                self.__arm.remove_all_missions()
                self.__arm.set_error_off()
                return

            print(len(self.__data_in))
            if len(self.__data_in) == 0:
                #stop generating
                self.msg_decision(bus)#send decision to run actuator

            current_target = self.__data_in.pop(0)
            print(f"current target: {current_target}")
            if self.__last_target is None:
                self.__last_target = current_target
            if type(current_target) is tuple:
                # print(f"going to {current_target}")
                self.__arm.move_to_with_segments(*current_target)
                pass
            else:
                self.__is_pen_down = True if current_target == 1 else False


        pass

    def quit(self):
        pass