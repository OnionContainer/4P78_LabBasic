import sympy
import sympy.vector
from sympy.geometry import Point2D as Point
import cv2
from typing import List, Tuple, Callable, Optional, Any
from datetime import datetime
import time
from VirtualArm.ArmMission import ArmMission, RegRotateMission, SegmentMovementMission
from Configer import configer

class VirtualArms:

    def force_set(self, motor1:int, motor2:int):
        self.__motorDegrees[0] = motor1
        self.__motorDegrees[1] = motor2

    def get_motor_interval(self, motor:int)->sympy.Interval:
        return self.__motorInterval[motor]

    def get_bar_length(self, motor:int)->float:
        return self.__barLength[motor]

    def get_motor_angle(self, motor:int)->float:
        return self.__motorDegrees[motor]

    def has_mission(self)->bool:
        return len(self.__updateFunction) > 0

    def get_current_mission(self)->ArmMission:
        return self.__updateFunction[0]

    def preempt_mission(self, mission:ArmMission):
        self.__updateFunction.insert(0,mission)

    def __init__(self):

        self.a_random_callback = None

        data = configer.get("VArm_config")

        self.__root: Point = Point()
        self.__motorDegrees: List[float] = data["init_motors"]
        self.__motorInterval: List[sympy.Interval] = [
            sympy.Interval(*data["intervals"][0]),
            sympy.Interval(*data["intervals"][1])
        ]

        # self.__motorInterval: List[sympy.Interval] = []
        #
        # for i in data["intervals"]:
        #     self.__motorInterval.append(sympy.Interval(i[0],i[1]))
        self.__barLength: List[float] = data["bar_length"]
        self.__motorSpeed: List[float] = data["motor_speed"]
        self.__noCrossPoints: List[Point] = []  # those are no crossing points
        self.__lastUpdateTime: datetime = datetime.now()

        # self.__updateFunction: Optional[
        #     Callable[[float], bool]] = None  # return true when registered action is complete
        #make it a list to spin different motors at the same time

        self.__updateFunction:List[ArmMission] = []
        self.__is_in_error = False
        #this is a list of executable functions that accepts delta time and returns bool

        print(self.__root)

    def remove_all_missions(self):
        self.__updateFunction.clear()

    def set_error(self):
        self.__is_in_error = True

    def set_error_off(self):
        self.__is_in_error = False

    def get_is_error(self):
        return self.__is_in_error

    def solve_angle_final(self, motor:int)->float:
        if motor == 0:
            return self.__motorDegrees[0]
        else:
            return self.__motorDegrees[motor] + self.solve_angle_final(motor-1)
        pass

    def solve_node_pos(self, node: int) -> tuple[float, float]:
        """
        Calculate the position of the specified node recursively:
        - 0: Return the root point.
        - 1: Return the position of the first motor.
        - 2: Return the position of the second bar's tip.

        Contributed by ChatGPT.
        """
        if node == 0:
            return self.__root.x, self.__root.y
        elif node > 0:
            prev_point = self.solve_node_pos(node - 1)
            angle = sum(self.__motorDegrees[:node])
            angle = sympy.rad(angle)
            x = prev_point[0] + self.__barLength[node - 1] * sympy.cos(angle).evalf()
            y = prev_point[1] + self.__barLength[node - 1] * sympy.sin(angle).evalf()
            return x,y
        else:
            raise ValueError("Invalid node index. Must be 0, 1, or 2.")

    def move_to_with_segments(self, x:float, y:float):
        self.__updateFunction.append(
            SegmentMovementMission(
                self,
                (x,y)
            )
        )

    def rotate(self, degree=0, motor=0):
        # rotate which motor clock wise in how many degrees
        # if not self.__updateFunction:
        #     print("VA: rotation command registration failed")
        #     return
        #this method does not care limitations

        target_degree = self.__motorDegrees[motor] + degree
        is_clockwise = degree > 0
        clockwise_factor = 1 if is_clockwise else -1

        mission = RegRotateMission(
            spd = self.__motorSpeed[motor],
            init_deg= self.__motorDegrees[motor],
            is_clockwise=clockwise_factor,
            target_degree=target_degree,
            motor_number=motor
        )

        self.preempt_mission(mission)

        # self.__updateFunction.append(mission)

        # check no passing point
        pass

    @staticmethod
    def get_move_to_optimized_plan(machine, x:float,y:float):
        #I am going to return RotatePlan it just not allowing me to type hit that
        #Also I am not able to hint VirtualArms?
        #@Earl

        m:VirtualArms = machine

        from VirtualArm.RotatePlan import RotatePlan
        from sympy import Point, Circle, deg, atan2, sqrt, solve, symbols

        # Step 1: Test if the target position is reachable
        target = Point(x, y)
        total_length = sum(m.__barLength)  # Total length of the arm
        distance = Point(0, 0).distance(target)  # Distance from the base to target

        if distance > total_length:
            print("Target point is too far and unreachable!")
            return

        if distance < abs(m.__barLength[0] - m.__barLength[1]):
            print("Target point is too close and unreachable!")
            return

        # Step 2: Set up intersection of circles for possible states
        base = Point(0, 0)  # Base point of the robotic arm
        l1, l2 = m.__barLength  # Length of the two bars (links)

        # Circle centered at the base with radius l1
        circle1 = Circle(base, l1)

        # Circle centered at the target with radius l2
        circle2 = Circle(target, l2)

        # Solve for the intersection points of the two circles
        intersection_points = circle1.intersection(circle2)

        if not intersection_points:
            print("No valid solutions found for the target point!")
            return

        plan_a = RotatePlan(m, intersection_points[0], Point(x, y))
        plan_b = RotatePlan(m, intersection_points[1], Point(x, y))

        best_plan = (None, float("inf"))
        for plan in plan_a.get_valid_plan():
            cost = RotatePlan.solve_plan_cost(plan)
            if cost < best_plan[1]:
                best_plan = (plan, cost)
        for plan in plan_b.get_valid_plan():
            cost = RotatePlan.solve_plan_cost(plan)
            if cost < best_plan[1]:
                best_plan = (plan, cost)

        if best_plan[0] is None:
            # print("No valid plan found!")

            return

        return best_plan

        pass

    def move_to_good(self, x=0.0, y=0.0, immediately = False)->bool:

        from VirtualArm.RotatePlan import RotatePlan

        optimized_plan:(RotatePlan, float) = VirtualArms.get_move_to_optimized_plan(self,x,y)
        if optimized_plan is None or optimized_plan[0] is None:
            print("No valid plan found!")
            return False
        if not immediately:
            self.rotate(optimized_plan[0][0], 0)
            self.rotate(optimized_plan[0][1], 1)
        else:
            self.force_set(
                self.get_motor_angle(0) + optimized_plan[0][0],
                self.get_motor_angle(1) + optimized_plan[0][1]
            )

        return True



    def solve_approaching_moves(self, target: Point) -> List[Tuple[str, int]]:
        # show how to rotate motors to move the tip from current point to the target.
        pass

    def planck_degree_rotate(self, degree=True, motor=0):
        # randomly move around 0-2 degree to specified direction.
        # Degree is the direction
        # True for positive, which is counter clock wise
        # Normal distribution
        pass

    def approach(self, target: Point):
        # Move the tip to the target point using plank degree rotate
        pass

    def update(self, delta):
        """

        :param delta:
        :return: True if not doing anything yet.
        """
        if not self.__updateFunction:
            # print("VA: no mission registered 0 ")
            return True

        if len(self.__updateFunction) == 0:
            # print("VA: no mission registered 1")
            return True

        mission = self.__updateFunction[0]
        mission_accomplished = mission.execute(delta)
        mission_suggested_degree = mission.get_motor_degree()
        mission_suggested_motor = mission.get_focused_motor()
        if mission_suggested_degree is not None and mission_suggested_motor is not None:
            self.__motorDegrees[mission_suggested_motor] \
                = mission_suggested_degree

        if mission_accomplished:
            self.__updateFunction.pop(0)

        return False


if __name__ == "__main__":

    arm = VirtualArms()
    arm.rotate(380)

    while True:
        time.sleep(1)
        arm.update()
