from TransferProtocol import Transfer
import time  # Required to use delay functions

tp = Transfer('com6')

while True:
    tp.send(int(input()))
    time.sleep(0.5)