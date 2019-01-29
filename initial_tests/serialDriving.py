from TransferProtocol import TransferProtocol
import time

tp = TransferProtocol(port='com5')

while True:
    speed = int(input('Input speed: '))
    #direction = int(input('Input direction: '))+127
    tp.send(speed.to_bytes(1,'big'))
    #ArduinoSerial.write(direction.to_bytes(1, 'big'))
