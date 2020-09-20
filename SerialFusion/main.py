import serial
ser = serial.Serial("COM4", 9600)

while True:
    cc = ser.readline().decode().strip()
    print(cc)