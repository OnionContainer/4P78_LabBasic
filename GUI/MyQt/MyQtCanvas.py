from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt


class MyQtCanvas(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)  # 创建 QPainter 对象

        painter.setBrush(QBrush(QColor("#f0f0f0")))  # 灰色背景
        painter.drawRect(self.rect())  # 绘制填充的矩形
        painter.fillRect(self.rect(), QColor("#ff00f0"))

        # 设置画笔（颜色、线宽、线型）
        pen = QPen(QColor(0, 0, 255))  # 蓝色
        pen.setWidth(2)  # 线宽 2 像素
        pen.setStyle(Qt.SolidLine)  # 实线

        painter.setPen(pen)  # 应用画笔
        painter.drawLine(20, 20, 100, 100)  # 画一条线段

        # 画一个矩形
        painter.drawRect(50, 50, 200, 100)  # (x, y, 宽度, 高度)

        # 画一个圆
        painter.drawEllipse(100, 150, 50, 50)  # (x, y, 直径, 直径)
