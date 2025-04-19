import serial
import serial.tools.list_ports

def list_ports():
	ports = serial.tools.list_ports.comports()
	return [p.device for p in ports]

def main():
	print("==== ESP32 Stepper Motor Bluetooth Control ====")
	available = list_ports()
	print("Available Ports", available)

	port = input("Select Port to Connect:").strip()
	ser = serial.Serial(port, baudrate=115200, timeout=2)

	while True:
		user_input = input("Steps to turn(negative means another direction):").strip()
		if user_input.lower() == "q":
			break
		try:
			steps = int(user_input)
			ser.write(f"{steps}\n".encode())
			print(f"sent:{steps}")
		except ValueError:
			print("Input invalid")

	ser.close()
	print("Port Closed")

if __name__ == "__main__":
	main()
