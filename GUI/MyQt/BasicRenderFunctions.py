from typing import List, Tuple

from PyQt5.QtGui import QPen, QColor

from GUI.MyQt.MyQtGView import MyQtGView


class BasicRenderFunctions:

    def __init__(self, canvas: MyQtGView):
        self._canvas = canvas

    def clear_canvas(self, tags=("point", "line")):
        if type(tags) is str:
            tags = (tags,)
        for item in self._canvas.scene().items():
            # Check if the item contains any of the matching tags
            if item.data(0) in tags:
                self._canvas.scene().removeItem(item)

    def sign_line(self, point1=(0.0, 0.0), point2=(1.0, 1.0), width=1.1, fill="red", tag="line"):
        pen = QPen(QColor(fill))
        pen.setWidthF(width)
        line = self._canvas.scene().addLine(point1[0], point1[1], point2[0], point2[1], pen)
        line.setData(0, tag)
        return line

    def get_canvas_scroll_and_scale(self):
        horizontal_scroll = self._canvas.horizontalScrollBar().value()
        vertical_scroll = self._canvas.verticalScrollBar().value()
        scale = self._canvas.transform().m11()  # Assuming uniform scaling
        return {"horizontal_scroll": horizontal_scroll, "vertical_scroll": vertical_scroll, "scale": scale}

    def sign_points(self, points: List[Tuple[float, float]], tag="point", message=None, shift=None, width=3.5):
        # Iterate over all points in the list and plot them using self._canvas
        for x, y in points:
            # Assuming self._canvas has a method to draw or mark points,
            # replace 'draw_point' with the correct method name if necessary
            point = self._canvas.scene().addEllipse(x - width / 2, y - width / 2, width, width)
            point.setData(0, tag)

    def report_canvas_status(self):
        print(f"current element count: {len(self._canvas.scene().items())}")

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

    def sign_text(self, text:str, position:Tuple[int,int], font_size:int=14, fill="black", tag="text"):
        x, y = position
        font = self._canvas.scene().font()
        font.setPointSize(font_size)
        text_item = self._canvas.scene().addText(text, font)
        text_item.setDefaultTextColor(QColor(fill))
        text_item.setPos(x, y)
        text_item.setData(0, tag)