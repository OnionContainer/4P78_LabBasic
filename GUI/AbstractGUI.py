from abc import ABC, abstractmethod
from typing import Tuple, List, Callable
import numpy as np


class AbstractGUI(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def sign_line_graph(self, data:List[float], position:Tuple[int,int], tag="line_graph"):
        pass

    @abstractmethod
    def sign_text(self, text, position, font_size=14, fill="black", tag="text"):
        pass

    @abstractmethod
    def get_life_game_renderer(self, cell_color_dict:dict, game_size:Tuple[int,int], display_position:Tuple[float, float] = (0,0)):
        pass

    @abstractmethod
    def draw_np_array_as_game_of_life_frame(self, data: np.ndarray, name:str, position:Tuple[int,int]):
        pass

    @abstractmethod
    def add_button(self, text, callback):
        pass

    @abstractmethod
    def mainloop(self, update_callback:Callable[[], None]):
        pass

    @abstractmethod
    def rebind_entry_receiver(self, callback):
        pass

    @abstractmethod
    def sign_rect(self, point1, point2, width, fill, tag="rect"):
        pass

    @abstractmethod
    def clear_fans(self):
        pass

    @abstractmethod
    def draw_fan_contour(self, x, y, radius, start_angle, extent, outline_color, width, tag="fan"):
        pass

    @abstractmethod
    def coordinate_centering_filter(self, point: Tuple[float, float]) -> Tuple[float, float]:
        pass

    @abstractmethod
    def sign_point(self, point, tag="point", message=None, shift=None):
        pass

    @abstractmethod
    def sign_points(self, points: List[Tuple[float, float]], tag="point", message=None, shift=None, width=1.5):
        pass

    @abstractmethod
    def report_canvas_status(self):
        pass

    @abstractmethod
    def sign_line(self, point1=(0.0, 0.0), point2=(1.0, 1.0), width=1.1, fill="red", tag="line"):
        pass

    @abstractmethod
    def clear_canvas(self, tags=("point", "line")):
        pass

    @abstractmethod
    def on_return_key(self, event):
        pass
