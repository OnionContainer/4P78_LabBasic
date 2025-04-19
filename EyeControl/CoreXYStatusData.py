import math
from sympy import Interval
"""
This is a data class that stores the status of a CoreXY machine.

angleMotorA: float(current rotation position of motor A)
angleMotorB: float(current rotation position of motor B)

motorRadius: float(radius of the motor)

positionX: float(current position of X axis) (determined by system state)
positionY: float(current position of Y axis) (determined by system state)

xRange: float(range of X axis)
yRange: float(range of Y axis)

AngleMotorA_Range: float(range of motor A) (determined by system state)
AngleMotorB_Range: float(range of motor B) (determined by system state)
"""

class CoreXYStatusData:
    def __init__(self, angle_motor_a=0.0, angle_motor_b=0.0, motor_radius=1.0, 
                 position_x=0.0, position_y=0.0, x_range=Interval(-100,100), y_range=Interval(-100,100),
                 angle_motor_a_range=Interval(-360,360), angle_motor_b_range=Interval(-360,360)):
        """
        Initializes the CoreXYStatusData class with default or specified values.
    
        Parameters:
        angle_motor_a (float): The current rotation position of motor A (default is 0.0).
        angle_motor_b (float): The current rotation position of motor B (default is 0.0).
        motor_radius (float): The radius of the motor in units (default is 1.0).
        position_x (float): The current position on the X-axis (default is 0.0).
        position_y (float): The current position on the Y-axis (default is 0.0).
        x_range (float): The maximum range of the X-axis (default is 100.0).
        y_range (float): The maximum range of the Y-axis (default is 100.0).
        angle_motor_a_range (float): The range of motor A angles in degrees (default is 360.0).
        angle_motor_b_range (float): The range of motor B angles in degrees (default is 360.0).
        """
        
        self._angleMotorA = angle_motor_a
        self._angleMotorB = angle_motor_b
        self._motorRadius = motor_radius
        self._positionX = position_x
        self._positionY = position_y
        self._xRange = x_range
        self._yRange = y_range
        self._angleMotorA_Range = angle_motor_a_range
        self._angleMotorB_Range = angle_motor_b_range

    def get_position(self):
        return self._positionX, self._positionY

    def get_angle(self):
        return self._angleMotorA, self._angleMotorB

    def force_set_zero(self):
        """
        set current position/angle to zero
        :return:
        """
        self._positionX = 0
        self._positionY = 0
        self._angleMotorA = 0
        self._angleMotorB = 0

    def turn_motor(self, turn_a, turn_b)->bool:

        target_angle_motor_a = self._angleMotorA + turn_a
        target_angle_motor_b = self._angleMotorB + turn_b
        if target_angle_motor_a not in self._angleMotorA_Range or target_angle_motor_b not in self._angleMotorB_Range:
            return False

        arc_a = (turn_a / 360) * 2 * math.pi * self._motorRadius
        arc_b = (turn_b / 360) * 2 * math.pi * self._motorRadius
        

        dx = (arc_a - arc_b)/2
        dy = (arc_a + arc_b)/2
        
        target_position_x = self._positionX + dx
        target_position_y = self._positionY + dy

        if target_position_x not in self._xRange or target_position_y not in self._yRange:
            return False

        self._angleMotorA = target_angle_motor_a
        self._angleMotorB = target_angle_motor_b
        self._positionX = target_position_x
        self._positionY = target_position_y

        return True

    def __str__(self):
        return (f"Motor A Angle: {self._angleMotorA:.2f}, Motor B Angle: {self._angleMotorB:.2f}\n"
                f"X Position: {self._positionX:.2f}, Y Position: {self._positionY:.2f}\n"
                f"X Range: {self._xRange}, Y Range: {self._yRange}\n"
                f"Motor Radius: {self._motorRadius:.2f}")


if __name__ == "__main__":
    corexy = CoreXYStatusData()
    print("Welcome to the CoreXY Interactive Test")
    print(corexy)

    while True:
        print("\nOptions:")
        print("1. Get the current position")
        print("2. Get the current motor angles")
        print("3. Turn the motors")
        print("4. Display the current status")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            print("Current Position:", corexy.get_position())
        elif choice == '2':
            print("Current Motor Angles:", corexy.get_angle())
        elif choice == '3':
            try:
                turn_a_ = float(input("Enter rotation for Motor A (degrees): "))
                turn_b_ = float(input("Enter rotation for Motor B (degrees): "))
                if corexy.turn_motor(turn_a_, turn_b_):
                    print("Motors turned successfully.")
                else:
                    print("Failed to turn motors. Check ranges or positions.")
                print(corexy)
            except ValueError:
                print("Invalid input! Please enter numeric values.")
        elif choice == '4':
            print(corexy)
        elif choice == '5':
            print("Exiting the test. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")