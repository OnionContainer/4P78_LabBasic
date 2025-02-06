

class Message:
    def __init__(self, publisher, info):
        self.__publisher = publisher
        self.__info = info
        self.__had_been_read = False
        """
        self.__publisher = the object that generated the message
        self.__info = the message, in key-value form
        """

    def is_read(self):
        return self.__had_been_read

    def set_read(self):
        self.__had_been_read = True

    def get_info(self):
        return self.__info

    def get_publisher(self):
        return self.__publisher

class MessageBus:
    def __init__(self):
        self.__messages = []

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
        # self.__messages.append(content)
        pass

    def iterate_messages(self):
        pass

    def delete_message(self, message:Message):
        pass


