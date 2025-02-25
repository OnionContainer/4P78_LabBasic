import time
import tkinter as tk
from typing import List, Tuple
from Configer import configer

"""

graphic here, interactive in coordinateDrawer

"""



class MyTk(tk.Tk):
    def __init__(self):
        super().__init__()
        # print("no?")
        config = configer.get("window_setup")

        self.width = config["width"]
        self.height = config["height"]
        self.geometry(f"{self.width}x{self.height + 50}+0+0")

        self.title(config.get("title"))
        
        canvas_width, canvas_height = config["canvas_size"]
        self.__canvas_width, self.__canvas_height = canvas_width, canvas_height
        
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.grid(row=0, column=0)
        

        # self.canvas.create_line(self.width // 2, 0, self.width // 2, self.height, fill="black")  # Y-axis
        # self.canvas.create_line(0, self.height // 2, self.width, self.height // 2, fill="black")  #
        self.canvas.create_line(canvas_width // 2, 0, canvas_width // 2, canvas_height, fill="black")  # Y-axis
        self.canvas.create_line(0, canvas_height // 2, canvas_width, canvas_height // 2, fill="black")  #

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=0)
        self.entry.bind("<Return>", self.on_return_key)
        self.entry.focus_set()
        self.__entry_receiver = lambda x: print(x)

        

        self.__auto_center = config["auto_center"]
        self.__x_shift = config["x_shift"]
        self.__y_shift = config["y_shift"]
        self.__x_scale = config["x_scale"]
        self.__y_scale = config["y_scale"]
        
        # self.sign_point((-105,115), "origin", "object location", (0,30))
        # # 扇形测试，从 -30° 开始
        # x, y = 200, 200  # 圆心坐标
        # r = 100  # 半径
        # self.canvas.create_arc(x - r, y - r, x + r, y + r,
        #                   start=-30, extent=10, outline="red", width=2)

    def rebind_entry_receiver(self, callback):
        self.__entry_receiver = callback

    def clear_fans(self):
        self.canvas.delete("fan")

    def draw_fan_contour(self, x, y, radius, start_angle, extent, outline_color, width, tag="fan"):

        x,y = self.coordinate_centering_filter((x,y))

        x0, y0 = x - radius, y - radius
        x1, y1 = x + radius, y + radius



        # start_angle *= -1
        # extent *= -1

        # print(f"start_angle: {start_angle}, extent: {extent}")

        # 使用 create_arc 绘制扇形轮廓
        self.canvas.create_arc(
            x0, y0, x1, y1,
            start=start_angle,  # 起始角度
            extent=extent,  # 绘制范围
            outline=outline_color,  # 轮廓颜色
            fill='',  # 无填充
            width=width,# 线宽
            tags=tag
        )

    def coordinate_centering_filter(self, point:Tuple[float,float])->Tuple[float,float]:

        if self.__auto_center:
            __x_shift = self.__canvas_width // 2.0
            __y_shift = self.__canvas_height // 2.0

            return point[0] + __x_shift, point[1] + __y_shift
        else:
            return point[0]*self.__x_scale + self.__x_shift, point[1]*self.__y_scale + self.__y_shift

    def sign_point(self, point, tag="point", message=None, shift=None):
        self.sign_points([point], tag, message, shift)

    def sign_points(self, points: List[Tuple[float, float]], tag="point", message = None, shift=None, width=1.5):
        """
        Draw the given points on the canvas.
        :param points: List of (x, y) tuples representing points to draw
        """
        # Clear the canvas first
        # self.canvas.delete("point")  # Line commented to retain previously drawn points
        # print(points)

        for x, y in points:
            # Store the point data for reference or future use
            # Adjust points to canvas coordinates (centered at the middle)
            # x,y = self.coordinate_centering_filter((x,y))
            # canvas_x = self.width // 2 + x
            # canvas_y = self.height // 2 - y

            canvas_x,canvas_y = self.coordinate_centering_filter((x,y))

            # Draw the point (a small oval)
            self.canvas.create_oval(
                canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5,
                fill="#f03099", outline="#000000", tags=tag
            )

            self.canvas.create_text(
                canvas_x + 10 if shift is None else canvas_x + shift[0],
                canvas_y - 15 if shift is None else canvas_y + shift[1],
                text=f"({x:.1f}, {y:.1f})" if message is None else message,
                fill="red",
                tags=tag,
                font = ("Arial", 10),  # Font & size
            )

        # Update the canvas
        self.canvas.update()

    def sign_line(self, point1=(0.0,0.0), point2=(1.0,1.0), width=1.1, fill="red", tag="line"):
        #draw a line from point 1 to point 2
        # self.canvas.delete("line")
        point1 = self.coordinate_centering_filter(point1)
        point2 = self.coordinate_centering_filter(point2)
        self.canvas.create_line(point1, point2, fill=fill, tags=tag, smooth=True, width=width)
        pass

    def clear_canvas(self, tags=("point", "line")):
        if type(tags) is str:
            self.canvas.delete(tags)
            return
        for tag in tags:
            self.canvas.delete(tag)

    def on_return_key(self, event):
        """
        Handle the 'Return' key press event for the text entry field.
        """
        input_value = self.entry.get()
        # print(f"Entered text: {input_value}")
        self.entry.delete(0, tk.END)  # Clear the entry field
        self.__entry_receiver(input_value)
        return input_value
        

if __name__ == "__main__":

    mytk = MyTk()
    mytk.sign_point((0,0))
    mytk.mainloop()

