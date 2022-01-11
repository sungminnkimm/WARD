import os
import sys
import time
import datetime
import RPi.GPIO as GPIO


GAPTIME = 3
PIR = 11

DETECTED = 1 # PIR == 0
NOT_DETECTED = 0 # PIR == 1

state = 'LOW' ## LOW, FALLING_EDGE, RISING_EDGE, HIGH

new_val = 0

#queue = circularQueue.CircularQueue()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIR, GPIO.IN)

print("Running detect_PIR_ver2.py...")
print("Waiting for PIR sensor to settle")
time.sleep(2)

def take_picture():
    print(">> take_picture() is called")
    now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    filepath = '/home/pi/offline_acousticIoT/images/'
    # cmd = "fswebcam -r 1280x720 --no-banner " + filepath + now + '.jpg'
    cmd = 'raspistill -t 1 -w 1280 -h 720 -o ' + filepath + now + '.jpg'
    filename = filepath + now + '.jpg'
    #print(filename)
    t1 = time.time()
    os.system(cmd)
    print(time.time()-t1)

if __name__ == '__main__':

    os.system('cp .asoundrc /home/pi/')
    print("---- main ----")
    f = open("/home/pi/offline_acousticIoT/detected.txt", 'a')

    try:
        while 1:
            cur_time = time.time()
            
            new_val = GPIO.input(PIR)

            if new_val == NOT_DETECTED:
                state = 'LOW'
            elif new_val == DETECTED:
                state = 'HIGH'
                print(">> elapsed time: ", time.time() - cur_time, state)
                t = datetime.datetime.fromtimestamp(cur_time)
                #print("timestamp: ", timestamp, "t: ", t)
                now = t.strftime('%Y%m%dT%H%M%S')
                f.write("%s\n"%now)
                take_picture()
                # print(">>    latest_time = ", datetime.datetime.fromtimestamp(cur_time))
                
            # print("one operation:", time.time() - cur_time)
          
    except KeyboardInterrupt:
        f.close()
        print('\n>>> detect_PIR_ver2.py Interrupted')
        print('\n>>> Exit detect_PIR_ver2.py...')
        sys.exit(0)