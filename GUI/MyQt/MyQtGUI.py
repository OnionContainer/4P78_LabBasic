from typing import List, Tuple, Callable

import numpy as np
from PyQt5.QtGui import QPen, QColor

from GUI.MyQt.MyQtCanvas import MyQtCanvas

from GUI.AbstractGUI import AbstractGUI

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QBoxLayout
from PyQt5.QtCore import QTimer

from GUI.MyQt.MyQtGView import MyQtGView
from GUI.MyQt.MyQtLineEdit import MyQtLineEdit
from GUI.MyQt.MyQtTestCanvas import MyQtTestCanvas


class MyQtGUI(AbstractGUI):

    def sign_line_graph(self, data: List[float], position: Tuple[int, int], tag="line_graph"):
        x_shift = position[0]
        y_interval = 50.
        for d in data:
            # print(d)
            self.sign_line(
                (x_shift, position[1]), (x_shift, position[1]-d*y_interval),
                tag=tag,
                width=1.5,
                fill=f"#{hex(min(int(d*1000), 255))[2:]}00{hex(min(int((1-d)*100), 255))[2:]}"
            )

            x_shift += 0.1
        pass

    def sign_text(self, text, position, font_size=14, fill="black", tag="text"):
        x, y = position
        font = self._canvas.scene().font()
        font.setPointSize(font_size)
        text_item = self._canvas.scene().addText(text, font)
        text_item.setDefaultTextColor(QColor(fill))
        text_item.setPos(x, y)
        text_item.setData(0, tag)

    def sign_rect(self, point1, point2, width, fill="black", tag="rect"):
        x1, y1 = point1
        x2, y2 = point2
        rect_x = min(x1, x2)
        rect_y = min(y1, y2)
        rect_width = abs(x2 - x1)
        rect_height = abs(y2 - y1)
    
        pen = QPen(QColor(fill))
        pen.setWidthF(width)
        brush = QColor(fill)
    
        rect = self._canvas.scene().addRect(rect_x, rect_y, rect_width, rect_height, pen)
        rect.setBrush(brush)
        rect.setData(0, tag)

    def draw_np_array_as_game_of_life_frame(self, data: np.ndarray, name:str, position:Tuple[int,int]):
        self.clear_canvas((name,))
        grid_size = 3.0#hot arg
        self.sign_rect(
            (position[0], position[1]),
            (position[0] + (data.shape[0]-1) * grid_size, position[1] + (data.shape[1]-1) * grid_size),
            grid_size,
            "black",
            name
        )
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                # print(f"Value at position ({i}, {j}): {data[i, j]}")
                c = data[i,j]
                if c == 0:
                    continue
                x = position[0] + i * grid_size
                y = position[1] + j * grid_size
                self.sign_line(
                    (x, y),
                    (x + 0.1, y),
                    grid_size,
                    "red" if c == 1 else "blue",
                    name
                )

    def add_button(self, text, callback):
        pass
        print("add button")
        button = QPushButton(text)
        button.clicked.connect(callback)
        print(self._button_layout is None)
        print(self._order_test)
        self._button_layout.addWidget(button)

    def _prepare_window(self):
        print("prepare window")
        self._order_test = "prepare"
        self._app = QApplication(sys.argv)

        self._window = QWidget()
        self._window.resize(800, 600)
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

        self._buttons = [[QPushButton(f"Button {r + 1}-{c + 1}") for c in range(2)] for r in range(4)]

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

        # button_layout = QGridLayout()
        # button_layout = QBoxLayout(QBoxLayout.TopToBottom)
        # self._button_layout = button_layout
        # # print(button_layout)
        # for r in range(1):
        #     for c in range(2):
        #         # button_layout.addWidget(self._buttons[r][c], r, c)
        #         button_layout.addWidget(self._buttons[r][c])
        #         pass
        # layout.addLayout(button_layout, 0, 1, 2, 1)  # 按钮列在右侧
        # self._window.setLayout(layout)
        # self._window.setLayout(button_layout)  # Ensure that layout is accessible for add_button

        button_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self._button_layout = button_layout
        print(self._button_layout)
        for r in range(1):
            for c in range(2):
                # button_layout.addWidget(self._buttons[r][c], r, c)
                self._button_layout.addWidget(self._buttons[r][c])
                pass
        layout.addLayout(self._button_layout, 0, 1, 2, 1)  # 按钮列在右侧
        self._window.setLayout(layout)
        self._window.setLayout(self._button_layout)  # Ensure that layout is accessible for add_button

        self.sign_line((-180,-180), (-180,280), 3, "red", "coordinate")
        self.sign_line((-180, -180), (280, -180), 3, "red", "coordinate")
        self.sign_line((280, -180), (280, 280), 3, "red", "coordinate")
        self.sign_line((-180, 280), (280, 280), 3, "red", "coordinate")
        pass

    def mainloop(self, update_callback: Callable[[], None]):
        self._main_timer = QTimer()
        # self._timer.timeout.connect(rrr)
        print(type(self._main_timer.timeout))
        self._main_timer.timeout.connect(update_callback)
        self._main_timer.start(10)

        print("mainloop called")
        print(self._button_layout)

        sys.exit(self._app.exec_())
        pass

    def rebind_entry_receiver(self, callback):
        self._entry.rebind_enter_callback(callback)

    def clear_fans(self):
        pass

    def draw_fan_contour(self, x, y, radius, start_angle, extent, outline_color, width, tag="fan"):
        pass

    def coordinate_centering_filter(self, point: Tuple[float, float]) -> Tuple[float, float]:
        pass

    def sign_point(self, point, tag="point", message=None, shift=None):
        print(f"\n\n\n\nsign_point: {point}\n\n\n\n")
        pass

    def sign_points(self, points: List[Tuple[float, float]], tag="point", message=None, shift=None, width=3.5):
        # Iterate over all points in the list and plot them using self._canvas
        for x, y in points:
            # Assuming self._canvas has a method to draw or mark points, 
            # replace 'draw_point' with the correct method name if necessary
            point = self._canvas.scene().addEllipse(x - width / 2, y - width / 2, width, width)
            point.setData(0, tag)


    def sign_line(self, point1=(0.0, 0.0), point2=(1.0, 1.0), width=1.1, fill="red", tag="line"):
        pen = QPen(QColor(fill))
        pen.setWidthF(width)
        line = self._canvas.scene().addLine(point1[0], point1[1], point2[0], point2[1], pen)
        line.setData(0, tag)

    def clear_canvas(self, tags=("point", "line")):
        # if True:
        #     return
        # print(self.get_canvas_scroll_and_scale())
        # Iterate over all items in the canvas scene
        if type(tags) is str:
            tags = (tags,)
        for item in self._canvas.scene().items():
            # Check if the item contains any of the matching tags
            if item.data(0) in tags:
                self._canvas.scene().removeItem(item)

    def on_return_key(self, event):
        pass

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
        # print("MyQtGUI init")
        super().__init__()
        self._prepare_window()
        print(self)
    
    def get_canvas_scroll_and_scale(self):
        horizontal_scroll = self._canvas.horizontalScrollBar().value()
        vertical_scroll = self._canvas.verticalScrollBar().value()
        scale = self._canvas.transform().m11()  # Assuming uniform scaling
        return {"horizontal_scroll": horizontal_scroll, "vertical_scroll": vertical_scroll, "scale": scale}


