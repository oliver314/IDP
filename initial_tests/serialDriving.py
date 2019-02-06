from TransferProtocol import Transfer
import time

tp = Transfer(port='com5')

while True:
    angle = int(input('Input angle: '))
    #direction = int(input('Input direction: '))+127
    tp.send(angle)
    #ArduinoSerial.write(direction.to_bytes(1, 'big'))
