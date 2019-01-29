import serial  # Serial imported for Serial communication
import time  # Required to use delay functions

ArduinoSerial = serial.Serial('com5', 9600)  # Create Serial port object called arduinoSerialData
time.sleep(2)  # wait for 2 secounds for the communication to get established

print('Listening...')


while True:
    speed = int(input('Input speed: '))
    #direction = int(input('Input direction: '))+127
    ArduinoSerial.write(speed.to_bytes(1,'big'))
    #ArduinoSerial.write(direction.to_bytes(1, 'big'))
