import tkinter as tk

class ViewDraggableCanvas(tk.Canvas):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)

		# 逻辑缩放因子
		self.zoom = 1.0

		# 设置初始 scrollregion（用于拖动）
		self.configure(scrollregion=(-1000, -1000, 1000, 1000))

		# 绑定事件
		self.bind("<ButtonPress-1>", self._on_mouse_press)
		self.bind("<B1-Motion>", self._on_mouse_drag)
		self.bind("<MouseWheel>", self._on_mouse_wheel)

	def _on_mouse_press(self, event):
		self.scan_mark(event.x, event.y)

	def _on_mouse_drag(self, event):
		self.scan_dragto(event.x, event.y, gain=1)

	def _on_mouse_wheel(self, event):
		# 缩放因子
		scale = 1.1 if event.delta > 0 else 0.9
		self.zoom *= scale

		# 在鼠标位置缩放所有图形
		self.scale("all", event.x, event.y, scale, scale)

		# 更新 scrollregion 区域
		self.configure(scrollregion=self.bbox("all"))

	def draw_circle(self, x, y, r, **kwargs):
		"""在逻辑坐标下绘制圆，自动应用缩放"""
		x *= self.zoom
		y *= self.zoom
		r *= self.zoom
		return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
