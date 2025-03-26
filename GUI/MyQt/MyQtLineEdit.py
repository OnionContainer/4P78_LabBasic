# Importing the Callable type from the typing module to type the callback parameter and attribute.
from typing import Callable

from PyQt5.QtWidgets import QLineEdit

# A custom QLineEdit subclass that supports registering a callback function,
# which gets triggered when the user presses the Enter/Return key.
class MyQtLineEdit(QLineEdit):
    # Initializes the custom QLineEdit widget with an optional callback function.
    # Parameters:
    #   callback: A function that takes a string (user input) as an argument and performs some action.
    #   *args, **kwargs: Any additional arguments passed to the QLineEdit constructor.
    def __init__(self, callback:Callable[[str], None] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if callback is None:
            # Default callback logs input to the console if no custom callback is provided.
            callback = lambda x: print(f"Line Edit Enter Event Not Registered, uncaught input: {x}")
        self._callback:Callable[[str], None] = callback

    # Allows the user to rebind the callback function to a new one after initialization.
    # Parameter:
    #   callback: A new function to replace the existing Enter key callback.
    def rebind_enter_callback(self, callback:Callable[[str], None]):
        self._callback = callback

    # Handles key press events and triggers the callback when the Enter/Return key is pressed.
    # The callback function is called with the current text in the line edit, and the input is cleared afterward.
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # Import the Qt module to access key-specific constants like Enter/Return keys.
        from PyQt5.QtCore import Qt
        # Check if the pressed key is Enter/Return and if a valid callback function is registered.
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and callable(self._callback):
            self._callback(self.text())
            self.clear()

