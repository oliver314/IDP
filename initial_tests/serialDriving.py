from TransferProtocol import Transfer
import time

tp = Transfer(port='com5')

while True:
    angle = int(input('Input command: '))
    tp.send(angle)

