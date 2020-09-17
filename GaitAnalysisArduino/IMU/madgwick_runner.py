import serial
import math
from madgwick import MadgwickAHRS

ser = serial.Serial('COM4')

line = ser.readline().decode('utf-8').strip().split(',')
gyx, gyy, gyz = math.radians(float(line[1])), math.radians(float(line[2])), math.radians(float(line[3]))
acx, acy, acz = float(line[4]), float(line[5]), float(line[6])
mgx, mgy, mgz = float(line[7]), float(line[8]), float(line[9])

heading = MadgwickAHRS()
while True:
    heading.update([gyx, gyy, gyz], [acx, acy, acz], [mgx, mgy, mgz])
    ahrs = heading.quaternion.to_euler_angles()
    roll = ahrs[0]
    pitch = ahrs[1]
    yaw = ahrs[2]
    print(f'Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}')