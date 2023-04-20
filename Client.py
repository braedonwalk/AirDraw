import serial
import time

#Inspired from 
#https://kevinponce.com/blog/python/send-gcode-through-serial-to-a-3d-printer-using-python/

class Client:
    def __init__(self, port, baud) -> None:
        '''
        Initialises the serial port and wakes up GRBL with desired settings.
        :param port: specify the port to which your printer is connected.
                    If it is an Arduino CNC shield, check the port from Arduino IDE
        :param baud: specify the baudrate at which GRBL is communicating. 
        '''
        self.ser = serial.Serial(port, baud)
        time.sleep(2)

        #Keeping track of the position in absolute values
        self.value_X = 0.0
        self.value_Y = 0.0

        self.__initialise("$X")
        self.__initialise("M3 S150")
        self.__initialise("M5 G4 P0.5")
        self.__initialise("$H")
        self.__initialise("F250")

        self.__initialise("G92 X0 Y0")
        # self.__initialise("G28 X0 Y0 Z0\r\n")
        # self.__initialise("G28 X0 Y0\r\n")
        # self.__initialise("G28 X0\r\n")
        # self.__initialise("G28 Y0\r\n")
        # self.__initialise("G28 Z0\r\n")

        # Absolute Mode
        self.__initialise("G90")
        self.__initialise("G94")
        self.__initialise("G17\r\n")

        # Set Units(does not seem to work on ender 5)
        self.__initialise("G20\r\n") # inches
        # self.__initialise("G21") # millimeters


    def command(self, cmd):
        '''
        Interfaces the Gcode commands to GRBL
        :param cmd:  A Gcode String.
        '''
        try:
            cmd = cmd.upper()
            # subcmds = cmd.split(" ")
            # for subcmd in subcmds:
            #     if subcmd[0] == "X":
            #         self.value_X += float(subcmd[1:])
            #     elif subcmd[0] == "Y":
            #         self.value_Y += float(subcmd[1:])
            # print(f'Value of X: {self.value_X}, Y: {self.value_Y}')
            cmd = cmd + "\r\n"
            self.ser.write(str.encode(cmd))
            # time.sleep(1)
            self.get_feedback()
        except TypeError:
            print("Gcode commands must be a string")


    def __initialise(self, cmd):
        '''
        Same as that of command but for initialisation. Used in the constructor.
        '''
        cmd = cmd + "\r\n"
        self.ser.write(str.encode(cmd))
        time.sleep(1)
        self.get_feedback()

    def flush(self):
        '''
        Use this function to close the serial port.
        '''
        time.sleep(2)
        self.ser.close()
        quit()

    def manual_mode(self):
        '''
        Use this for sending one command at a time.
        '''
        while True:
            string = input("Enter your Gcode: ")
            string = string.upper()
            print(string)
            if string == "Q":
                self.flush()
            
            else:
                self.command(string)

    def get_feedback(self):
        while True:
            feedback = self.ser.readline()
            # print(feedback)
            if feedback == b'ok\r\n':
                break