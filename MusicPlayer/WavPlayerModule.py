

from AbstractModule import AbstractModule
from MessageBus import MessageBus
from MusicPlayer.simple_wav_player import PlayerPlayer

"""
    <-msg   actuator_report
    <-cmd   play
"""
class WavPlayerModule(AbstractModule):

    def cmd_play(self, args=None):
        self.__player.set_playing(-1)

    def prep(self, register_cmd_callback):
        self.__player.start()
        register_cmd_callback("play", self.cmd_play)
        pass

    def update(self, dtime: float):

        #get the first "actuator_report" message. If no such message do nothing
        if actuator_report := self._peek_message("actuator_report") is not None:
            is_start = actuator_report["is_start"]
            self.__player.set_playing(is_start)

    def quit(self):
        pass

    def __init__(self, bus: MessageBus):
        super().__init__(bus)
        self.__player = PlayerPlayer()