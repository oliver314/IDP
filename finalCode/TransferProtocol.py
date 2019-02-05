import serial  # Serial imported for Serial communication
import time  # Required to use delay functions

class Transfer(object):
    def __init__(self, port='com5'):
        # Establishes connection with Arduino
        print('Establishing connection with Arduino')
        self.AS = serial.Serial(port, 9600)  # Create Serial port object called arduinoSerialData
        time.sleep(2)  # wait for 2 secounds for the communication to get established
        print('Connected successfully')

    def read(self):
        # Returns most recent byte in buffer
        val = None
        while self.AS.in_waiting:
            val = self.AS.read()
            val = int.from_bytes(val, byteorder='big')
            print("Values in Serial buffer: " +str(val))
        return val

    def readline(self):
        # Returns most recent line in buffer
        line = None
        while self.AS.in_waiting:
            line = self.AS.readline()
        return line.rstrip()

    def send(self, val):
        if type(val) is int:
            try:
                self.AS.write(val.to_bytes(1, byteorder='big'))
            except:
                print("Couldn't send value "+ str(val))
        else:
            print('Value must be an integer')
