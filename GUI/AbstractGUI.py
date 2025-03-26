from abc import ABC, abstractmethod
from typing import Tuple, List, Callable


class AbstractGUI(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def mainloop(self, update_callback:Callable[[], None]):
        pass

    @abstractmethod
    def rebind_entry_receiver(self, callback):
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
    def sign_line(self, point1=(0.0, 0.0), point2=(1.0, 1.0), width=1.1, fill="red", tag="line"):
        pass

    @abstractmethod
    def clear_canvas(self, tags=("point", "line")):
        pass

    @abstractmethod
    def on_return_key(self, event):
        pass
