from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPoint

class MyQtGView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        scene = QGraphicsScene(self)
        # rect = QGraphicsRectItem(0, 0, 100, 100)
        # scene.addItem(rect)
        # scene.addItem(
        #     QGraphicsRectItem(300, 0, 300, 300)
        # )
        # scene.addItem(
        #     QGraphicsRectItem(700, 700, 300, 300)
        # )
        self.setScene(scene)
        # self.setDragMode(QGraphicsView.NoDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scene.setSceneRect(-200, -200, 500, 500)



    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        oldPos = self.mapToScene(event.pos())

        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        newPos = self.mapToScene(event.pos())
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event):
        # self._mousePressPos = self.mapToScene(event.pos()).toPoint()  # 记录鼠标按下的位置
        # print("pressed")
        # # self.setTransformationAnchor(QGraphicsView.NoAnchor)
        # # self.translate(10,10)
        # ee = self.mapToScene(event.pos()).toPoint()  # 记录鼠标按下的位置
        # self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - 10)
        # self.verticalScrollBar().setValue(self.verticalScrollBar().value() - 10)
        super(QGraphicsView, self).mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:  # 左键按住并移动鼠标
    #         mouseMovePos = self.mapToScene(event.pos()).toPoint()  # 记录鼠标位置
    #         moved = mouseMovePos - self._mousePressPos  # 计算位移
    #         self.setTransformationAnchor(QGraphicsView.NoAnchor)  # 设置缩放中心点为视图左上角，即不变
    #         self.translate(-moved.x(), -moved.y())  # 根据位移量平移视图
    #     super(QGraphicsView, self).mouseMoveEvent(event)

    