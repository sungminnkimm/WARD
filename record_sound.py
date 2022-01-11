import os
import time
import datetime
import sys



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
    
    # os.system('cp .asoundrc /home/pi/offline_a')
    time.sleep(2)
    os.system('pkill -ef -9 arecord')

    try:
        while 1:
            cur = time.time()
            record_sound() ## record continuously for 5 sec
            time.sleep(0.5)
            print(time.time() - cur)

    except KeyboardInterrupt:
        print("\nrecord_sound.py Interrupted")
        print("\n>>> Exit record_sound.py...")
        sys.exit(0)
        
        
    
