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
            self.__raw_command = cmd
            print(f"hi! i got {cmd}")
        self.__window.rebind_entry_receiver(update_raw_cmd)

        pass


    def __quit(self):
        for module in self.__modules:
            module.quit()

    def execute_current_command(self):
        if not self.__raw_command:
            return
        cmd = self.__raw_command.split(" ")
        if not cmd[0] in self.__command_map:
            print(f"no command found: {self.__raw_command}")
            self.__raw_command = ""

        self.__command_map[cmd[0]](cmd[1:])

    def register_command(self):
        pass

    def prep(self):

        """
        prepare every other modules
        """

        example = ExampleModule()
        self.__modules.append(example)


        self.update()
        self.__window.mainloop()
        pass

    def update(self):
        t = time()
        dtime = t - self.__last_update_time
        self.__last_update_time = t
        #calculate delta time

        """
        read from terminal for commands
        
        """
        
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