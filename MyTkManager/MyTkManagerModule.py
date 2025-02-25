from AbstractModule import AbstractModule
from MyTk import MyTk
from MessageBus import MessageBus
import tkinter as tk

class MyTkManagerModule(AbstractModule):

    def on_register_button(self, info):
        print(f"register button: {info}")
        my_window:tk.Tk = self.__my_tk
    
        button_text = info.get("text", "Default Text")
        button = tk.Button(self.__frame, text=button_text, command=info.get("callback", lambda:print("click")))
        # button.grid(row=len(self.__button_list), column=1)
        button.grid(row = len(self.__button_list), column = 0)
        self.__button_list.append(button)

    def prep(self, register_cmd_callback):
        print("prep my tk manager")


        my_window: tk.Tk = self.__my_tk
        my_window.update_idletasks()  # Ensure all widgets are updated before calculating dimensions
        highest_element_height = max(widget.winfo_height() for widget in my_window.grid_slaves(row=0))
        
        frame = tk.Frame(my_window, bg="dark blue", bd=1, highlightbackground="red", highlightthickness=1, width=10, height=highest_element_height)
        frame.grid(row=0, column=1, sticky="n")
        self.__frame = frame

        self.on_register_button({"text": "Hello"})
        self.on_register_button({"text": "Hellw"})
        self.on_register_button({"text": "Helle"})
        self.on_register_button({"text": "Hella"})

        pass

    def update(self, dtime: float):

        if (info := self._peek_message("register_button")) is not None:
            self.on_register_button(info)

        # if info := self._peek_message("register_button") is not None:
        #     self.on_register_button(info)


        pass

    def quit(self):
        pass

    def __init__(self, bus:MessageBus, my_tk:MyTk):
        super().__init__(bus)
        self.__my_tk = my_tk
        self.__button_list = []
        self.__frame = None


    