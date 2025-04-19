from AbstractModule import AbstractModule
from ColorfulGameOfLife.AbstractColorfulGameOfLife import RuleSet, CellType
from ColorfulGameOfLife.MyColorfulGameOfLife import MyColorfulGameOfLife
from GUI.AbstractGUI import AbstractGUI
from GUI.MyQt.MyQtGUI import MyQtGUI
from MyTk import MyTk
from MessageBus import MessageBus
import tkinter as tk
import numpy as np
from Logger.Logger import Logger, hot
from ColorfulGameOfLife.FunctionTimer import timeit


class GUIModule(AbstractModule):

    def on_register_button(self, info:dict):
        # print(f"register button: {info}")
        self.__gui_object.add_button(
            info.get("text", "Default Text"),
            info.get("callback", lambda: print("click button"))
        )

    def prep(self, register_cmd_callback):

        self.on_register_button({
            "text": "Restart Game",
            "callback": self.init_game
        })

        def prg():
            self.playing = not self.playing
            if self.playing:
                self.stepping = -1

        self.on_register_button({
            "text": "Pause/Resume Game",
            "callback": prg
        })

        def stp():
            self.stepping = 1

        self.on_register_button({
            "text": "Step",
            "callback": stp
        })

        def other():
            self._i_want_another_game = not self._i_want_another_game
            self.init_game()

        self.on_register_button({
            "text": "I want another cell",
            "callback": other
        })

        def vani():
            self._is_vanilla = not self._is_vanilla
            self.init_game()

        self.on_register_button({
            "text": "Vanilla?",
            "callback": vani
        })

        pass

    def init_game(self):
        r = RuleSet()
        if self._is_vanilla:
            r.add_cell_type(CellType(#Conway Vanilla
                generate_condition={83},
                death_condition={80, 81, 84, 85, 86, 87, 88},
                contribution=11
            ))
        else:
            r.add_cell_type(CellType(#Day/Night
                generate_condition={83, 86, 87, 88},
                death_condition={80, 81, 82, 85},
                contribution=11
            ))

        # r.add_cell_type(CellType(#HighLife
        #     generate_condition={82},
        #     death_condition={80, 83, 84, 85, 86, 87, 88},
        #     contribution=11
        # ))

        if self._i_want_another_game:
            r.add_cell_type(CellType(
                generate_condition={84},
                death_condition={70, 71, 75, 77, 80, 81, 82, 83, 84, 85, 87},
                contribution=11
            ))

        # print(r.get_cell_types_length())

        g = MyColorfulGameOfLife()
        g.setup_rule_set(r)
        self._game = g

        # print(g.get_recent_history_key_matrix())

    def iterate_game(self):

        self._game.iterate(1)

        if self._render_function is not None:
            self._render_function(self._game.get_recent_history_key_matrix())
        else:
            self._render_function = self.__gui_object.get_life_game_renderer(
                cell_color_dict={
                    0: "black",
                    1: "blue"
                },
                game_size = self._game.get_game_size(),
                display_position = (0,0)
            )

        # self.__gui_object.report_canvas_status()
        self.__gui_object.basic_render_functions.clear_canvas("try")

        self.__gui_object.basic_render_functions.sign_text(
            f"Change Rate: {self._game.get_recent_difference() * 100:.1f}%",
            (0,-30),
            font_size=4,
            tag="try"
        )

        self.__gui_object.sign_line_graph(
            self._game.get_difference_history()[0:self.max_observed_steps],
            (0, -10),
            "try",
        )


        if self._game.get_history_length() > self.max_observed_steps:
            difference_history = self._game.get_difference_history()[0:self.max_observed_steps]
            average_difference = np.mean(difference_history)  # Calculate the average
            self.__gui_object.basic_render_functions.sign_text(
                f"Average Change: {average_difference * 100:.1f}%",
                (0, -50),
                font_size=4,
                tag="try"
            )


    def update(self, dtime: float):

        # self.on_register_button({"text": "Hello"})

        # print(self.__gui_object)
        if self.playing and self.stepping == -1:
            self.iterate_game()
        elif self.stepping >= 1:
            self.stepping -= 1
            self.iterate_game()

        if (info := self._peek_message("register_button")) is not None:
            for i in info:
                self.on_register_button(i)


        # if info := self._peek_message("register_button") is not None:
        #     self.on_register_button(info)

        pass

    def quit(self):
        pass

    def __init__(self, bus: MessageBus, gui_object: MyQtGUI):
        super().__init__(bus)
        self.__gui_object = gui_object
        self._game = None
        self.playing = False
        self.stepping = -1
        self.max_observed_steps = 500
        self._i_want_another_game = False
        self._is_vanilla = True
        self._render_function = None

        self.init_game()



