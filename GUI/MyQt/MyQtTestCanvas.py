from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath
import sys

from fontTools.pens.qtPen import QtPen


class MyQtTestCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建场景
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # 设置场景大小 (比 View 大，触发滚动条)
        scene_width = 800
        scene_height = 600
        self._scene.setSceneRect(-200, -200, scene_width, scene_height)

        # 加载多个图片并放置到超出 View 边界的位置
        
        # # 创建一个 QtPen 对象
        # path = QPainterPath()
        # pen = QtPen(path)
        # path.moveTo(100, 100)
        # path.lineTo(200, 200)
        # path.lineTo(300, 150)
        # self.scene.addPath(path, pen)
        
        # Add a big rectangle to the scene
        # brush = QBrush(Qt.SolidPattern)
        # pen = QPen(Qt.black)
        # self._scene.addRect(
        #     -50, -50, scene_width + 100, scene_height + 100, pen, brush
        # )
        #
        # pen = QPen(Qt.red)
        # self._scene.addRect(
        #     50, 50, scene_width - 100, scene_height - 100, pen, brush
        # )
        
        # self.scene.addRect(
        #     0, 0, scene_width + 100, scene_height + 100,
        #     Qt.black, Qt.SolidPattern)
        # self.add_image("image1.png", 50, 50)   # 可见范围
        # self.add_image("image2.png", 500, 100) # 右侧超出
        # self.add_image("image3.png", 200, 400) # 下方超出
        # self.add_image("image4.png", 600, 500) # 右下角超出

        # 允许滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def add_image(self, image_path, x, y):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            item = QGraphicsPixmapItem(pixmap)
            item.setPos(x, y)
            self._scene.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MyQtTestCanvas()
    view.resize(400, 300)  # 视图窗口比场景小，触发滚动
    view.show()
    sys.exit(app.exec_())
