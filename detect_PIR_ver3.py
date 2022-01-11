import os
import sys
import time
import datetime
import RPi.GPIO as GPIO

print("Running detect_PIR_ver3.py...")
print("Waiting for PIR sensor to settle")
time.sleep(2)

def take_picture():
    print(">> take_picture() is called")
    now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    filepath = '/home/pi/offline_acousticIoT/images/'
    cmd = 'raspistill -t 1 -w 1280 -h 720 -o ' + filepath + now + '.jpg'
    filename = filepath + now + '.jpg'
    t1 = time.time()
    os.system(cmd)
    print(time.time()-t1)

if __name__ == '__main__':

    os.system('cp .asoundrc /home/pi/')
    print("---- main ----")

    try:
        while 1:
            cur_time = time.time()
            
            take_picture()
            time.sleep(3)

            print(time.time() - cur_time)
          
    except KeyboardInterrupt:
        print('\ndetect_PIR.py Interrupted')
        print('\n>>> Exit detect_PIR_ver3.py...')
        sys.exit(0)