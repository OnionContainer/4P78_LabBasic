from dataclasses import dataclass
from typing import Callable, TypeVar
from enum import Enum, auto
import this

from blinker import signal

class EventData:
    pass

@dataclass
class ERegisterButton(EventData):
    button_text: str
    button_function: Callable[[], None]

class SignalType(Enum):
    REGISTER_BUTTON = auto()
    DISPLAY_TEXT = auto()

EventDataChild = TypeVar("EventDataChild", bound=EventData)

class EventCenter:
    def __init__(self):
        self._signal_dict = {signal_type: signal(signal_type.name.lower()) for signal_type in SignalType}
        print(self._signal_dict)
        pass

    def emit(self, signal_name: SignalType, data: EventDataChild):
        self._signal_dict[signal_name].send(data)
        pass

    def on(self, signal_name: SignalType, callback: Callable[[EventDataChild], None]):
        self._signal_dict[signal_name].connect(callback)
        pass

ec = EventCenter()


def create_button(event:ERegisterButton):
    text = event.button_text
    callback = event.button_function
    print(f"{text}, {callback}")

ec.on(SignalType.REGISTER_BUTTON, create_button)

ec.emit(SignalType.REGISTER_BUTTON, ERegisterButton("test", lambda: print("test")))


def emit(signal_name: SignalType, data: EventDataChild):
    ec.emit(
        signal_name,
        data)
    pass


def on(signal_name: SignalType, callback: Callable[[EventDataChild], None]):
    ec.on(
        signal_name,
        callback)
    pass