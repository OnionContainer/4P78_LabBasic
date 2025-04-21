import serial
import time
import serial.tools.list_ports

def list_serial_ports():
	ports = serial.tools.list_ports.comports()
	return [port.device for port in ports]

def main():
	print("==== ESP32 Servo Motor Control） ====\n")

	# 列出可用串口
	available_ports = list_serial_ports()
	if available_ports:
		print("Avaliable Ports:")
		for p in available_ports:
			print(f" - {p}")
	else:
		print("⚠️ Port not detected")

	# 选择串口
	default_port = "COM6"
	com_port = input(f"\nEnter the Port name（default: {default_port}）: ").strip() or default_port

	# 尝试连接串口
	try:
		ser = serial.Serial(port=com_port, baudrate=115200, timeout=2)
		print(f"✅ connection success {com_port}")
	except Exception as e:
		print(f"❌ unable to open: {e}")
		return

	time.sleep(2)  # 等待 ESP32 启动

	try:
		while True:
			user_input = input("🎮 Enter two time values（like 500 -300），or q to quit: ").strip()
			if user_input.lower() in ('q', 'quit'):
				break

			parts = user_input.split()
			if len(parts) != 2:
				print("⚠️ Wrong syntax")
				continue

			try:
				time_a = int(parts[0])
				time_b = int(parts[1])
				cmd = f"{time_a} {time_b}\n"
				ser.write(cmd.encode())
				print(f"📤 sent: {cmd.strip()}")

				# # 可选：读取回传信息
				# response = ser.readline().decode().strip()
				# if response:
				# 	print(f"📥 收到: {response}")

			except ValueError:
				print("⚠️ Value Error")

	except KeyboardInterrupt:
		pass
	finally:
		ser.close()
		print("🔌 Port Closed")

if __name__ == "__main__":
	main()
