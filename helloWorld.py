import serial
from serial.tools import list_ports
import time
from datetime import datetime

def command(ser, command):
    start_time = datetime.now()
    command = command + '\r\n'
    ser.write(str.encode(command)) 
    time.sleep(1)

    while True:
        line = ser.readline()
        print(line)

        if line == b'ok\n':
            break

def initSender():
    return

def initGcode(ser):
    ser.write("M5 G4 P0.5")
    ser.write("$H")
    ser.write("G92X0Y0")
    ser.write("G20")
    ser.write("G1X0Y0F1000")


ser = serial.Serial('COM10', 115200)
