import os
import time
import datetime
import RPi.GPIO as GPIO

GAPTIME = 3
PIR = 11

DETECTED = 0 # PIR == 0
NOT_DETECTED = 1 # PIR == 1

state = 'LOW' ## LOW, FALLING_EDGE, RISING_EDGE, HIGH
latest_time = time.time()

old_val = 0
new_val = 0

#queue = circularQueue.CircularQueue()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIR, GPIO.IN)
print("Waiting for PIR sensor to settle")
time.sleep(2)

def take_picture():
    print(">> take_picture() is called")
    now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    filepath = '/home/pi/offline_acousticIoT/images/'
    # cmd = "fswebcam -r 1280x720 --no-banner " + filepath + now + '.jpg'
    cmd = 'raspistill -t 300 -w 1280 -h 720 -o ' + filepath + now + '.jpg'
    filename = filepath + now + '.jpg'
    #print(filename)
    os.system(cmd)

if __name__ == "__main__":
    os.system('cp .asoundrc /home/pi/')
    print("---- main ----")
    while 1:
        cur_time = time.time()
        
        new_val = GPIO.input(PIR)
                
        if old_val == NOT_DETECTED and new_val == NOT_DETECTED:
            state = 'LOW'
        elif old_val == NOT_DETECTED and new_val == DETECTED:
            state = 'RISING_EDGE'
        elif old_val == DETECTED and new_val == NOT_DETECTED:
            state = 'FALLING_EDGE'
        elif old_val == DETECTED and new_val == DETECTED:
            state = 'HIGH'
            
        #print("[", state,"] old = ",old_val, "new = ", new_val)
            
        old_val = new_val
        
        if(state == 'RISING_EDGE'):
            if(cur_time - latest_time > GAPTIME):
                print(">> elapsed time: ", cur_time - latest_time)
                latest_time = cur_time
                #queue.enqueue(latest_time)
                t = datetime.datetime.fromtimestamp(latest_time)
                #print("timestamp: ", timestamp, "t: ", t)
                now = t.strftime('%Y%m%dT%H%M%S')
                f = open("/home/pi/offline_acousticIoT/detected.txt", 'a')
                f.write("%s\n"%now)
                take_picture()
                print(">>    latest_time = ", datetime.datetime.fromtimestamp(latest_time))
            else:
                latest_time = cur_time
        elif(state == 'HIGH'):
            if(cur_time - latest_time > GAPTIME):
                print(">> elapsed time: ", cur_time - latest_time)
                latest_time = cur_time
                #queue.enqueue(latest_time)
                t = datetime.datetime.fromtimestamp(latest_time)
                #print("timestamp: ", timestamp, "t: ", t)
                now = t.strftime('%Y%m%dT%H%M%S')
                f = open("/home/pi/offline_acousticIoT/detected.txt", 'a')
                f.write("%s\n"%now)
                take_picture()
                print(">>    latest_time = ", datetime.datetime.fromtimestamp(latest_time))
            else:
                continue
        elif(state == 'FALLING_EDGE'):
            latest_time = cur_time
        