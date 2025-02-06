from time import time

from AbstractModule import AbstractModule
from ExampleModule import ExampleModule
from MessageBus import MessageBus
from MyTk import MyTk


class LabBasic:

    def __init__(self):
        self.__last_update_time = time()
        self.__modules:[AbstractModule] = []
        self.__bus = MessageBus()
        self.__command_map = {
            "quit": self.__quit
        }
        self.__raw_command = ""
        self.__window = MyTk()
        print("??")

        def update_raw_cmd(cmd):
            if self.__raw_command:
                print(f"raw command already exists: {self.__raw_command}")
                return
            self.__raw_command = cmd
            print(f"raw command: {cmd}")
        self.__window.rebind_entry_receiver(update_raw_cmd)

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


    def register_command(self):
        pass

    def prep(self):

        """
        prepare every other modules
        """

        example = ExampleModule()
        self.__modules.append(example)

        def register_cmd_callback(key, func):
            if self.__command_map.get(key):
                print(f"command {key} already registered")
                raise Exception(f"command {key} already registered")
            self.__command_map[key] = func

        for m in self.__modules:
            m.prep(register_cmd_callback)


        self.update()
        self.__window.mainloop()
        pass

    def update(self):
        t = time()
        dtime = t - self.__last_update_time
        self.__last_update_time = t
        #calculate delta time


        self.execute_current_command()
        
        try:
            for m in self.__modules:
                m.update(dtime, self.__bus)
            # self.execute_current_command()
            # map(lambda module: module.update(dtime, self.__bus), self.__modules)
        except Exception as e:
            print(e)

        self.__window.after(1000, self.update)

        pass

if __name__ == "__main__":
    print("?")
    lab = LabBasic()
    lab.prep()