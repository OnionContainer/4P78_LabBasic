from dataclasses import dataclass
from typing import Callable, TypeVar
from enum import Enum, auto
# import this

from blinker import signal

# Module Description: 
# This module implements a simple event-driven system using the `blinker` library.
# It provides a structure for defining event types, handling signals, and processing event data.

class EventData:
    # Base class to represent data associated with an event. All specific event data types should inherit from this class.
    pass


@dataclass
class ERegisterButton(EventData):
    """
    Event data for registering a button.

    Attributes:
        button_text (str): The text displayed on the button.
        button_function (Callable[[], None]): The function to be executed when the button is clicked.
    """
    button_text: str
    button_function: Callable[[], None]

@dataclass
class EyeData(EventData):
    eye_state: int
    eye_x: int
    eye_y: int

class SignalType(Enum):
    """
    An enumeration of signal types for the event system.

    Enums:
        REGISTER_BUTTON: Signal for registering a button.
        DISPLAY_TEXT: Signal for displaying text.
    """
    REGISTER_BUTTON = auto()
    DISPLAY_TEXT = auto()
    EYE_DATA = auto()

EventDataChild = TypeVar("EventDataChild", bound=EventData)

class EventCenter:
    """
    Centralized event system for emitting and handling signals.

    Methods:
        emit: Emits a signal with associated event data.
        on: Subscribes a callback to a specific signal.
    """
    def __init__(self):
        """
        Initializes the EventCenter with a dictionary of signals mapped to signal types.
        """
        self._signal_dict = {signal_type: signal(signal_type.name.lower()) for signal_type in SignalType}
        print(self._signal_dict)

    def emit(self, signal_name: SignalType, data: EventDataChild):
        """
        Emits a signal with the specified data.

        Args:
            signal_name (SignalType): The type of the signal to emit.
            data (EventDataChild): The event data associated with the signal.
        """
        self._signal_dict[signal_name].send(data)

    def on(self, signal_name: SignalType, callback: Callable[[EventDataChild], None]):
        """
        Subscribes a callback to a signal.

        Args:
            signal_name (SignalType): The type of signal to connect the callback to.
            callback (Callable): The function to execute when the signal is emitted.
        """
        self._signal_dict[signal_name].connect(callback)

ec = EventCenter()


def create_button(event: ERegisterButton):
    """
    Handles the REGISTER_BUTTON event by extracting button properties.

    Args:
        event (ERegisterButton): The event data containing button properties.
    """
    text = event.button_text
    callback = event.button_function
    print(f"{text}, {callback}")

ec.on(SignalType.REGISTER_BUTTON, create_button)

ec.emit(SignalType.REGISTER_BUTTON, ERegisterButton("test", lambda: print("test")))


def emit(signal_name: SignalType, data: EventDataChild):
    """
    Wrapper function for emitting events through the EventCenter.

    Args:
        signal_name (SignalType): The signal type to emit.
        data (EventDataChild): The event data to pass along with the signal.
    """
    ec.emit(signal_name, data)


def on(signal_name: SignalType, callback: Callable[[EventDataChild], None]):
    """
    Wrapper function for subscribing callbacks to events via the EventCenter.

    Args:
        signal_name (SignalType): The signal type to subscribe the callback to.
        callback (Callable): The function to execute when the signal is emitted.
    """
    ec.on(signal_name, callback)


