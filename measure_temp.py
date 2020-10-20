from subprocess import getoutput
import time

while(True):
    temp = getoutput('vcgencmd measure_temp')
    print(temp)
    time.sleep(10)
