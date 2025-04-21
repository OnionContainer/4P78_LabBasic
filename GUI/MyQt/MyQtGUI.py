from typing import List, Tuple, Callable
import time
import numpy as np
from PyQt5.QtGui import QPen, QColor

from GUI.MyQt.BasicRenderFunctions import BasicRenderFunctions
from GUI.MyQt.MyQtCanvas import MyQtCanvas

from GUI.AbstractGUI import AbstractGUI

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QBoxLayout
from PyQt5.QtCore import QTimer

from GUI.MyQt.MyQtGView import MyQtGView
from GUI.MyQt.MyQtLineEdit import MyQtLineEdit
from GUI.MyQt.MyQtTestCanvas import MyQtTestCanvas
from GUI.MyQt.MyQtTextColBoxLayout import MyQtTextColBoxLayout, say
import pyqtgraph as pg

class MyQtGUI:

    def get_life_game_renderer_alt(self, cell_color_dict: dict, game_size: Tuple[int, int], display_position: Tuple[float, float] = (0, 0)):

        pass


    def get_life_game_renderer(self, cell_color_dict: dict, game_size: Tuple[int, int], display_position: Tuple[float, float] = (0, 0)):
        #initialize the frame
        grid_size = 3.0#hot
        cell_collection = []
        pen_dict = {}
        default_pen = QPen(QColor("white"))
        tag = f"{time.time():.4f}tag"
        for key, value in cell_color_dict.items():
            p = QPen(QColor(value))
            p.setWidthF(grid_size)
            pen_dict[key] = p


        for x in range(game_size[0]):
            cell_layer = []
            for y in range(game_size[1]):
                pos_x = x * grid_size + display_position[0]
                pos_y = y * grid_size + display_position[1]
                cell = self.basic_render_functions.sign_line(
                    (pos_x, pos_y),
                    (pos_x + 0.1, pos_y),
                    grid_size,#stroke width
                    "black",#color
                    tag = tag
                )
                cell_layer.append(cell)
                # cell_bucket = {}
                # for key, value in cell_color_dict.items():
                #     pos_x = x * grid_size + display_position[0]
                #     pos_y = y * grid_size + display_position[1]
                #     cell = self.basic_render_functions.sign_line(
                #         (pos_x, pos_y),
                #         (pos_x + 0.1, pos_y),
                #         grid_size,#stroke width
                #         value,#color
                #         "cell"
                #     )
                #     cell_bucket[key] = cell
                #     cell.setVisible(False)
                # cell_layer.append(cell_bucket)
            cell_collection.append(cell_layer)

        def render(frame: np.ndarray, destroy = False):
            if destroy:
                self.basic_render_functions.clear_canvas((tag,))
                return
                pass
            #render the frame
            for x0 in range(game_size[0]):
                for y0 in range(game_size[1]):

                    cell_collection[x0][y0].setPen(
                        pen_dict.get(frame[x0, y0],default_pen)
                    )
                    # for key0, cell0 in cell_collection[x0][y0].items():
                    #     if key0 == frame_value:
                    #         cell0.setVisible(True)
                    #     else:
                    #         cell0.setVisible(False)
            pass

        return render
        pass

    def sign_line_graph(self, data: List[float], position: Tuple[int, int], tag="line_graph"):
        x_shift = position[0]
        y_interval = 50.
        for d in data:
            self.basic_render_functions.sign_line(
                (x_shift, position[1]), (x_shift, position[1]-d*y_interval),
                tag=tag,
                width=1.5,
                fill=f"#{hex(min(int(d*1000), 255))[2:]}00{hex(min(int((1-d)*100), 255))[2:]}"
            )

            x_shift += 0.1
        pass


    # Archived Method
    #
    # def draw_np_array_as_game_of_life_frame(self, data: np.ndarray, name:str, position:Tuple[int,int]):
    #     self.basic_render_functions.clear_canvas((name,))
    #     grid_size = 3.0#hot arg
    #     self.basic_render_functions.sign_rect(
    #         (position[0], position[1]),
    #         (position[0] + (data.shape[0]-1) * grid_size, position[1] + (data.shape[1]-1) * grid_size),
    #         grid_size,
    #         "black",
    #         name
    #     )
    #     for i in range(data.shape[0]):
    #         for j in range(data.shape[1]):
    #             c = data[i,j]
    #             if c == 0:
    #                 continue
    #             x = position[0] + i * grid_size
    #             y = position[1] + j * grid_size
    #             self.basic_render_functions.sign_line(
    #                 (x, y),
    #                 (x + 0.1, y),
    #                 grid_size,
    #                 "red" if c == 1 else "blue",
    #                 name
    #             )

    def add_button(self, text, callback):
        pass
        button = QPushButton(text)
        button.clicked.connect(callback)
        self._button_layout.addWidget(button)

    def _prepare_window(self):
        print("prepare window")
        self._order_test = "prepare"
        self._app = QApplication(sys.argv)

        self._window = QWidget()
        self._window.resize(1600, 600)
        self._window.setWindowTitle("My GUI")
        self._window.show()

        # 创建 UI 组件
        # self._canvas = MyQtCanvas(self._window)
        self._canvas = MyQtGView(self._window)
        # self._canvas = MyQtTestCanvas(self._window)

        # self._canvas.setStyleSheet("""

        #             margin: 10px;
        #             padding: 5px;
        #             border: 2px solid black;
        #             background-color: lightgray;
        #             font-size: 14px;
        #         """)
        # self._canvas.setFixedSize(500, 500)
        self._entry = MyQtLineEdit(None, self._window)
        self._entry.setMaximumWidth(500)

        self._buttons = []
        # self._buttons = [[QPushButton(f"Button {r + 1}-{c + 1}") for c in range(2)] for r in range(4)]

        # 布局
        layout = QGridLayout()
        layout.addWidget(self._canvas, 0, 0, 1, 1)  # Canvas 左侧大区域
        layout.addWidget(self._entry, 1, 0, 1, 1)  # Entry 置于 Canvas 下方

        self._entry.setStyleSheet("""
                    margin: 10px;
                    padding: 5px;
                    border: 2px solid black;
                    background-color: lightgray;
                    font-size: 14px;
                """)

        button_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self._button_layout = button_layout
        # for r in range(1):
        #     for c in range(2):
        #         # button_layout.addWidget(self._buttons[r][c], r, c)
        #         self._button_layout.addWidget(self._buttons[r][c])
        #         pass
        layout.addLayout(self._button_layout, 0, 1, 2, 1)  # 按钮列在右侧

        text_layout = MyQtTextColBoxLayout()
        layout.addLayout(text_layout, 0, 2, 2, 1)

        self._window.setLayout(layout)
        self._window.setLayout(self._button_layout)  # Ensure that layout is accessible for add_button

        say("Hello", "This column is to display messages")
        pass

    def mainloop(self, update_callback: Callable[[], None]):
        self._main_timer = QTimer()
        # self._timer.timeout.connect(rrr)
        self._main_timer.timeout.connect(update_callback)
        self._main_timer.start(110)
        sys.exit(self._app.exec_())
        pass

    def rebind_entry_receiver(self, callback):
        self._entry.rebind_enter_callback(callback)











    def __init__(self):
        print("init my qt gui")
        self._buttons = None
        self._entry:MyQtLineEdit|None = None
        self._canvas:MyQtGView|None = None
        self._main_timer = None
        self._window = None
        self._app = None
        self._button_layout: QBoxLayout | None = None
        self._order_test = "init"
        self._prepare_window()

        self.basic_render_functions = BasicRenderFunctions(self._canvas)
    



