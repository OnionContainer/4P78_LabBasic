#Sample movement to ensure communication with the 3D printer
from typing import Tuple, List

import serial
import time

def printer_control(data: List[Tuple[int, int]]):
    port = 'COM3' #Set this to your actual COM port!
    baudrate = 115200  # Common baudrate for 3D printers, adjust if needed

    #loop through each tuple
    #for each tuple:
    #print(f"G0 X{t[0]}\n")
    #print(f"G0

    a = 'G0 X10 Y20'.encode('utf-8')
    b = b'G0 X10 Y20'

    print(a == b)

    result = [b'G91\n']

    pendown = b'G0 Z-10\n'
    penup = b'G0 Z10\n'
    is_pendown = True

    for t in data:
        if t[0] == -1:
            if is_pendown:
                result.append(penup)
                is_pendown = False
            else:
                result.append(pendown)
                is_pendown = True
            #this means z axis control
            continue
        result.append(f"G0 X{t[0]} Y{t[1]}\n".encode('utf-8'))
        # print(f"G0 X{t[0]}\n")
        # print(f"G0 Y{t[1]}\n")

    result.append(b'G90\n')

    print(result)

    try:
        # Open the serial connection
        ser = serial.Serial(port, baudrate, timeout=2)
        print(f"Connected to 3D printer on {port}")

        # Allow the printer to initialize
        time.sleep(2)

        for r in result:
            ser.write(r)
            time.sleep(1)

        #
        # # Send GCode to raise the tip by 10mm
        # ser.write(b'G91\n')  # Set to relative positioning
        # ser.write(b'G0 Z10\n')  # Move up by 10mm
        # time.sleep(1)
        #
        # # Send GCode to move along the positive X axis by 10mm
        # ser.write(b'G0 X10\n')  # Move 10mm in X direction
        # time.sleep(1)
        #
        # # Send GCode to lower the tip by 10mm
        # ser.write(b'G0 Z-10\n')  # Move down by 10mm
        # time.sleep(1)
        #
        # # Set back to absolute positioning (optional, for safety)
        # ser.write(b'G90\n')

        print("Commands sent successfully.")

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Connection closed.")
            
def generate_fake_data() -> List[Tuple[int, int]]:
    """
    Generate fake data for testing.
    Returns a list of tuples containing X and Y coordinates.
    Example: [(10, 20), (30, 40), (50, 60)]
    """
    fake_data = [(10, 20), (10, 0), (0, 10), (-1, 0), (-2, -2),(-1, 0)]
    return fake_data

# Generate fake data for testing
test_data = generate_fake_data()  # Call the fake data generation function

# Test the printer_control method with the fake data
printer_control(test_data)
