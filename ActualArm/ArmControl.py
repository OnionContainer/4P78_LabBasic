import serial
import time


class ArmControl:
    def __init__(self):
        # Initialize serial connection
        self.ser = serial.Serial('COM9', 115200, timeout=1)  # Update COM port if needed
        time.sleep(2)  # Wait for serial connection to initialize
        print(self.ser.readline().decode('utf-8').strip())  # Read initial response from device

        # Shoulder parameters
        self.shoulder_min_angle, self.shoulder_max_angle = 45, 210
        self.shoulder_min_pwm, self.shoulder_max_pwm = 75, 444

        # Elbow parameters
        self.elbow_min_angle, self.elbow_max_angle = 45, 225
        self.elbow_min_pwm, self.elbow_max_pwm = 75, 470

    # Function to convert angle to PWM
    def angle_to_pwm(self, angle, min_angle, max_angle, min_pwm, max_pwm):
        """Convert an angle to a corresponding PWM pulse value."""
        if angle < min_angle or angle > max_angle:
            raise ValueError(f"Angle {angle} out of range ({min_angle} to {max_angle})")

        # Scale the angle to PWM range
        pwm_value = min_pwm + (angle - min_angle) * (max_pwm - min_pwm) / (max_angle - min_angle)
        return int(round(pwm_value))

    # Function to send PWM values over serial
    def send_command(self, shoulder_pwm, elbow_pwm, z):
        # time.sleep(0.1)
        """Send shoulder and elbow PWM values to the serial device along with a Z value."""
        comm = f'{{{shoulder_pwm},{elbow_pwm},{z}}}\n'.encode('utf-8')
        self.ser.write(comm)

        time.sleep(0.1)  # Wait for response
        data = self.ser.readline()
        print(data.decode('utf-8').strip())
        # time.sleep(0.1)

    def process_order(self, order_tuple):
        try:
            # for a in order_tuple:
            #     print(type(a))

            # Get user input
            shoulder_angle = order_tuple[0]
            if shoulder_angle == -1:
                return

            elbow_angle = order_tuple[1]
            z = order_tuple[2]

            # Convert angles to PWM
            shoulder_pwm = self.angle_to_pwm(shoulder_angle, self.shoulder_min_angle, self.shoulder_max_angle, self.shoulder_min_pwm,
                                        self.shoulder_max_pwm)
            elbow_pwm = self.angle_to_pwm(elbow_angle, self.elbow_min_angle, self.elbow_max_angle, self.elbow_min_pwm, self.elbow_max_pwm)

            # Send the PWM values to the serial device
            self.send_command(shoulder_pwm, elbow_pwm, z)

        except ValueError as e:
            print(f"Invalid input: {e}. Please enter valid numerical values.")


if __name__ == "__main__":
    a = ArmControl()
    # a.process_order((80,70,1))

    # for i in range(25):
    #     a.process_order((i*10, 70, 1))

    a.process_order((90, 70, 1))

    # points = [45,90,135,180,225]

    # for i in points:
    #     t = (90, i, 1)
    #     print(t)
    #     a.process_order(t)

    for i in range(100):
        a.process_order((90, 70+i*0.1, 1))

    print("no")