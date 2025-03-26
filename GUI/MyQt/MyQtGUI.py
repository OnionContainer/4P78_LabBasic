from typing import List, Tuple, Callable

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

    def _prepare_window(self):
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
        button_layout = QBoxLayout(QBoxLayout.TopToBottom)
        for r in range(4):
            for c in range(2):
                # button_layout.addWidget(self._buttons[r][c], r, c)
                button_layout.addWidget(self._buttons[r][c])
                pass
        layout.addLayout(button_layout, 0, 1, 2, 1)  # 按钮列在右侧
        self._window.setLayout(layout)

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
        self._buttons = None
        self._entry:MyQtLineEdit|None = None
        self._canvas:MyQtGView|None = None
        self._main_timer = None
        self._window = None
        self._app = None
        # print("MyQtGUI init")
        super().__init__()
        self._prepare_window()
    
    def get_canvas_scroll_and_scale(self):
        horizontal_scroll = self._canvas.horizontalScrollBar().value()
        vertical_scroll = self._canvas.verticalScrollBar().value()
        scale = self._canvas.transform().m11()  # Assuming uniform scaling
        return {"horizontal_scroll": horizontal_scroll, "vertical_scroll": vertical_scroll, "scale": scale}


