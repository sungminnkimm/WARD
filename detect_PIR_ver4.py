import os
import sys
import time
import datetime

print("Running detect_PIR_ver4.py...")
print("\nWaiting for PIR sensor to settle")
time.sleep(3)

def take_picture():
    print(">> take_picture() is called")
    now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    filepath = '/home/pi/offline_acousticIoT/images/'
    cmd = 'raspistill -t 1 -w 1280 -h 720 -o ' + filepath + now + '.jpg'
    filename = filepath + now + '.jpg'
    t1 = time.time()
    os.system(cmd)
    print(time.time()-t1)

def record_sound():
    print(">> record_sound() is called")
    now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    filepath = '/home/pi/offline_acousticIoT/soundfiles/'
    record_cmd = 'arecord -D plughw:1,0 -r 44100 -t wav -f S16_LE -c 2 -d 3 ' + filepath + now + '.wav'
    #record_cmd = 'arecord -D plughw:2,0 -r 8000 -t wav -d 5 ' + filepath + now + '.wav'
    filename = filepath + now + '.wav'
    print(filename)
    os.system(record_cmd)


if __name__ == '__main__':

    os.system('cp .asoundrc /home/pi/')
    os.system('pkill -ef -9 arecord')

    print("---- main ----")

    task_count = 0

    try:
        while 1:
            cur_time = time.time()
            print(">>>>> take_picture()")
            take_picture()
            print(">>>>> picture taken", time.time() - cur_time)
            print(">>>>> record_sound")
            record_sound()
            task_count += 1
            print(str(task_count) + " tasks done", time.time() - cur_time)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print('\n>>> Keyboard Interrupted')
        print('\n>>> Exit detect_PIR_ver4.py...')
        sys.exit(0)