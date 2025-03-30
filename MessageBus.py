

"""
message: actuator_report
content: {
    "type": "actuator_report",
    "is_start"(bool): true if actuator starts, false if it stops,
    "key"(data type): description
}

message: register_button
content: {
    "type": "register_button",
    "text"(str): text you want to display in the button,
    "callback"(callable): function you want to call when button pressed
}

message: display_text(not implemented yet)
content: {
    "type": "display_text",
    "position"(tuple): position of text block,
    "text"(str): text you want to display,
    "id"(str): id of text block,
}
"""

class Message:
    def __init__(self, publisher, info):
        self.__publisher = publisher
        self.__info = info
        self.__is_checked = False
        """
        self.__publisher = the object that generated the message
        self.__info = the message, in key-value form
        """

    def print(self):
        print(f"publisher: {self.__publisher}, info: {self.__info}")

    def is_read(self):
        return self.__is_checked

    def set_checked(self):
        self.__is_checked = True

    def get_info(self):
        return self.__info

    def get_publisher(self):
        return self.__publisher

class MessageBus:
    def __init__(self):
        self.__messages = []

    function_dict = {}

    @staticmethod
    def register_event(event_key, func):
        if MessageBus.function_dict.get(event_key) is None:
            MessageBus.function_dict[event_key] = []
        else:
            MessageBus.function_dict[event_key].append(func)

    @staticmethod
    def emit_event(event_key, info):
        if MessageBus.function_dict.get(event_key) is None:
            print(f"No listener for event key: {event_key}")
            return False
        else:
            for func in MessageBus.function_dict[event_key]:
                func(info)
            return True

    def push_message(self, publisher, content):
        """
        :param publisher: type = Any, the object that is publishing the message
        :param content: type = dict, json format message
        Example:
        {
            "type": "movement request",
            "motor0": 330,
            "motor1": 130,
            "penup": True
        }
        and the controlling module can test if the type is what it wants and
        execute if yes.
        :return:
        """
        m = Message(publisher, content)
        self.__messages.append(m)
        pass

    def delete_all_checked_messages(self):
        self.__messages = [m for m in self.__messages if not m.is_read()]
        
    def get_length(self):
        return len(self.__messages)

    def iterate_messages(self):
        return iter(self.__messages)

    def delete_message(self, message:Message):
        """
        explicitly delete a message whether it is checked or not
        :param message:
        :return:
        """
        self.__messages.remove(message)
        pass


