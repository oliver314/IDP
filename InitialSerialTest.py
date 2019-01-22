import serial  # Serial imported for Serial communication
import time  # Required to use delay functions

ArduinoSerial = serial.Serial('com5', 9600)  # Create Serial port object called arduinoSerialData
time.sleep(2)  # wait for 2 secounds for the communication to get established

print("Enter 1 to turn ON LED and 0 to turn OFF LED")

while True:  # Do this forever

    var = input()  # get input from user

    if (var == '1'):  # if the value is 1
        ArduinoSerial.write(b'a')  # send a
        print("LED turned ON")
        time.sleep(1)

    if (var == '0'):  # if the value is 0
        ArduinoSerial.write(b'b')  # send b
        print("LED turned OFF")
        time.sleep(1)