from TransferProtocol import Transfer
import keyboard
from time import sleep

tp = Transfer('com5')

print('Press space to begin calibration')
while not keyboard.is_pressed(' '):
    pass
sleep(2)

def frontTest():
    print('Closing front')
    tp.send(0)
    while not keyboard.is_pressed(' '):
        pass
    tp.send(1)
    sleep(1)
    val = tp.read()
    print('fClose: ' + str(val))
    sleep(1)

    print('Opening front')
    tp.send(2)
    while not keyboard.is_pressed(' '):
        pass
    tp.send(3)
    sleep(1)
    val = tp.read()
    print('fOpen: ' + str(val))
    sleep(1)

def backTest():
    print('Opening back')
    tp.send(4)
    while not keyboard.is_pressed(' '):
        pass
    tp.send(5)
    sleep(1)
    val = tp.read()
    print('bOpen: ' + str(val))
    sleep(1)

    print('Closing back')
    tp.send(6)
    while not keyboard.is_pressed(' '):
        pass
    tp.send(7)
    sleep(1)
    val = tp.read()
    print('bClose: ' + str(val))
    sleep(1)

frontTest()