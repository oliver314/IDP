import serial  # Serial imported for Serial communication
import time  # Required to use delay functions

class TransferProtocol(object):
    def __init__(self,port='com5'):
        # Establishes connection with Arduino
        print('Establishing connection with Arduino')
        self.AS = serial.Serial(port, 9600)  # Create Serial port object called arduinoSerialData
        time.sleep(2)  # wait for 2 secounds for the communication to get established
        print('Connected successfully')

    def read(self):
        # Returns most recent value in buffer
        print('Checking buffer')
        val = None
        while self.AS.in_waiting():
            val = self.AS.read()
        return val

    def send(self,val):
        if val.is_int():
            self.write(val.to_bytes(1, 'big'))
        else:
            print('Value must be an integer')

