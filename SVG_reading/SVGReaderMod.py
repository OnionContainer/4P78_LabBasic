from AbstractModule import AbstractModule
from MessageBus import MessageBus
from Configer import configer
from SVG_reading.read_Image import drawSVG
from copy import deepcopy

"""

    ->msg   generate    plan
    <-cmd   bulk set    bset
    ->msg   bulk set    bset
"""
class SVGReaderMod(AbstractModule):
    def __init__(self, bus:MessageBus):
        super().__init__(bus)
        self.__reader = None
        self.__data = configer.get("SVG_reader_setup")
        self.__output_svg_data = None
        self.__is_output_data_drawn = False
        self.__is_generate_ready = False
        self.__is_bulk_set_mode = False

    def cmd_bulk_set(self):
        self.__is_generate_ready = True
        self.__is_bulk_set_mode = True
        pass

    def cmd_generate_rotation_plan(self, arg=None):
        self.__is_generate_ready = True
        self.__is_bulk_set_mode = False

    def cmd_preprocess_output_data(self, arg=("-110", "70")):
        x_shift = int(arg[0])
        y_shift = int(arg[1])
        new_data = []
        for line in self.__output_svg_data:
            if type(line) is tuple:
                new_data.append((line[0]+x_shift, line[1]+y_shift))
            else:
                new_data.append(line)
        self.__output_svg_data = new_data
        self.__is_output_data_drawn = False
        pass

    def __get_some_svg(self, filename=("shapes.svg", "cat.svg")):
        print(f"filename: {filename}")
        try:
            ree = drawSVG(filename[0], is_quiet=True)
            self.__output_svg_data = ree.plot()
            print(self.__output_svg_data)
            self.__is_output_data_drawn = False
            # print(self.__output_svg_data)
        except FileNotFoundError as e:
            print(f"{e}")
        pass

    def function_to_call(self):
        print("function called")

    def prep(self, register_cmd_callback):
        self.__reader = drawSVG(self.__data["default_SVG_file"], is_quiet=True)
        self.__output_svg_data = self.__reader.plot()

        register_cmd_callback("svg", self.__get_some_svg)
        register_cmd_callback("pp", self.cmd_preprocess_output_data)
        register_cmd_callback("plan", self.cmd_generate_rotation_plan)
        register_cmd_callback("bset", self.cmd_bulk_set)

        register_cmd_callback(
            "hello",
            self.function_to_call
        )


        pass

    def update(self, dtime: float):
        # print("svg updating")

        def send_draw_request():

            to_draw = []
            for line in self.__output_svg_data:
                if type(line) is tuple:
                    to_draw.append(line)

            # bus.push_message(self, {
            #     "type": "draw_request",
            #     "points": to_draw
            # })
            self._push_message({
                "type": "draw_request",
                "points": to_draw
            })

        if self.__output_svg_data is not None and not self.__is_output_data_drawn:
            # bus.push_message(self, {
            #     "type": "svg_cashtype_data",
            #     "content": self.__output_svg_data
            # })
            print(hasattr(self, "__push_message"))
            self._push_message({
                "type": "svg_cashtype_data",
                "content": self.__output_svg_data
            })
            send_draw_request()
            print("draw request sent")
            self.__is_output_data_drawn = True

        if self.__is_generate_ready and not self.__is_bulk_set_mode:
            self._push_message({
                "type": "generate_ready",
                "content": deepcopy(self.__output_svg_data)  # this should be deep copy ideally
            })
            self.__is_generate_ready = False

        if self.__is_generate_ready and self.__is_bulk_set_mode:
            # bus.push_message(self, {
            #     "type": "bulk_set",
            #     "content": deepcopy(self.__output_svg_data)
            # })
            self._push_message({
                "type": "bulk_set",
                "content": deepcopy(self.__output_svg_data)
            })
            self.__is_generate_ready = False

    def quit(self):
        pass

if __name__ == "__main__":
    mod = SVGReaderMod()
    mod.prep(lambda x,y: print(x,y))

