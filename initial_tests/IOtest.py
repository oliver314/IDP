from TransferProtocol import Transfer
import time  # Required to use delay functions

tp = Transfer('com5')

while True:
    tp.send(int(input()))
    time.sleep(0.5)