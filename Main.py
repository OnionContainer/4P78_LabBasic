from ActualArm.ArmControlModule import ArmControlModule
from Configer import configer
from time import time

from AbstractModule import AbstractModule
from ExampleModule import ExampleModule
from GUI.GUIModule import GUIModule
from MessageBus import MessageBus
from MusicPlayer.WavPlayerModule import WavPlayerModule
from MyTk import MyTk
from MyTkManager.MyTkManagerModule import MyTkManagerModule
from SVG_reading.SVGReaderMod import SVGReaderMod
from Test.TestModule import TestModule
from VirtualArm.VirtualArmModule import VirtualArmModule
from GUI.MyQt.MyQtGUI import MyQtGUI
from GUI.AbstractGUI import AbstractGUI

class LabBasic(AbstractModule):

    def quit(self):
        pass

    def __init__(self):
        self.__bus = MessageBus()
        super().__init__(self.__bus)

        # a = {"a": "b"}
        # p(f"[green]{a}[/green]")
        self.__last_update_time = time()
        self.__modules:[AbstractModule] = []
        self.__command_map = {
            "quit": self.__quit
        }
        self.__raw_command = ""
        # self.__window:AbstractGUI = MyTk()
        self.__window:MyQtGUI = MyQtGUI()
        # print("??")



        pass


    def __quit(self):
        print("quit")
        for module in self.__modules:
            module.quit()

    def execute_current_command(self):
        if not self.__raw_command:
            return
        cmd = self.__raw_command.split(" ")

        if not cmd[0] in self.__command_map:
            print(f"no command found: {self.__raw_command}")
            self.__raw_command = ""

        self.__raw_command = ""

        try:
            if len(cmd) == 1:
                self.__command_map[cmd[0]]()
            else:
                self.__command_map[cmd[0]](cmd[1:])
        except TypeError as e:
            print(e)
        except KeyError as e:
            print(f"[green]{e}[/green]")

    def register_command(self):
        pass

    def prep(self, register_cmd_callback=None):

        """
        prepare every other modules
        """
        gui_module = GUIModule(self.__bus, self.__window)
        self.__modules.append(gui_module)
        # svg = SVGReaderMod(self.__bus)
        # self.__modules.append(svg)
        # virArm = VirtualArmModule(self.__bus)
        # self.__modules.append(virArm)
        # control = ArmControlModule(self.__bus)
        # self.__modules.append(control)
        player = WavPlayerModule(self.__bus)
        self.__modules.append(player)
        # tk_manager = MyTkManagerModule(self.__bus, self.__window)
        # self.__modules.append(tk_manager)
        test_module = TestModule(self.__bus)
        self.__modules.append(test_module)



        def _register_cmd_callback(key, func):
            if self.__command_map.get(key):
                print(f"command {key} already registered")
                raise Exception(f"command {key} already registered")
            self.__command_map[key] = func

        for m in self.__modules:
            m.prep(_register_cmd_callback)

        def update_raw_cmd(cmd):
            if self.__raw_command:
                print(f"raw command already exists: {self.__raw_command}")
                return
            self.__raw_command = cmd
            print(f"raw command: {cmd}")
        self.__window.rebind_entry_receiver(update_raw_cmd)

        self.__window.mainloop(self.update)
        pass

    def update(self, dtime=None, bus=None):
        # print("#############################")
        t = time()
        dtime = t - self.__last_update_time
        self.__last_update_time = t
        #calculate delta time


        self.execute_current_command()
        
        try:
            for m in self.__modules:
                m.update(dtime)
            # self.execute_current_command()
            # map(lambda module: module.update(dtime, self.__bus), self.__modules)
        except Exception as e:
            raise e

        """
        messages to be resolved in main level
        """
        draw_request = self._peek_message("draw_request")
        if draw_request is not None:
            for request in draw_request:
                self.__window.clear_canvas("svg_draw")
                self.__window.sign_points(request["points"], tag="svg_draw", message="")

        text_request = self._peek_message("display_text")
        if text_request is not None:
            for request in text_request:
                self.__window.clear_canvas(request['id'])
                self.__window.sign_text(
                    request['text'],
                    request['position'],
                    font_size=4,
                    tag = request['id']
                )


        arm_render_request = self._peek_message("render_my_arm")
        if arm_render_request is not None:
            info = arm_render_request
            self.__window.clear_canvas("arm_render")

            for l in info["limits"]:
                self.__window.draw_fan_contour(**l, tag="arm_render")
            pp = None
            for p in info["points"]:
                if pp is None:
                    pp = p
                self.__window.sign_line(pp, p, tag="arm_render")
                pp = p

            # print("points!!!")
            self.__window.sign_points(info["points"], tag="arm_render")

        # print(self.__bus.get_length())
        self.__bus.delete_all_checked_messages()
        # print(self.__bus.get_length())
        # print(f"message remaining: {self.__bus.get_length()}")

        pass

if __name__ == "__main__":
    print(configer.get("name"))
    # print("?")
    lab = LabBasic()
    lab.prep()