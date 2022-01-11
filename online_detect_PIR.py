import os
import time
import datetime
import requests
import base64
#import circularQueue

import RPi.GPIO as GPIO
import time
import glob

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

url_Mobius = 'http://[64:FF9B::CBFD:80AC]:7579'

headers = {
   'Accept': 'application/json',
   'X-M2M-RI': '123sdfg45',
   'X-M2M-Origin': 'S20170717074825768bp21',
   'Content-Type': 'application/json; ty=4'
}

def send_acoustic_data_to_Mobius(url, con_acoustic, startTime, endTime):
    
    #print(">>    startTime = ", datetime.datetime.fromtimestamp(startTime))
    #print(">>    endTime = ", datetime.datetime.fromtimestamp(endTime))
    print("start time: ", startTime, "end_time: ", endTime)
    list_of_acoustic_files = glob.glob('/home/pi/offline_acousticIoT/soundfiles/*.wav')
    selected_files = []
    
    for f in list_of_acoustic_files:
        #print(os.path.getctime(f))
        if (os.path.getctime(f) > startTime and os.path.getctime(f) < endTime):
            selected_files.append(f)
            
    #print(selected_files)
    selected_files = sorted(selected_files, key = os.path.getctime)
    for f in selected_files:
        pass
    #print("***********************")
    print(selected_files)
    
    for f in selected_files:
        encoded_data = wavTobase64(f)
        post_to_Mobius(url, con_acoustic, encoded_data)
    


def send_image_data_to_Mobius(url, con_image, timestamp):
    t = datetime.datetime.fromtimestamp(timestamp)
    #print("timestamp: ", timestamp, "t: ", t)
    now = t.strftime('%Y%m%dT%H%M%S')
    filename = '/home/pi/offline_acousticIoT/images/' + now + '.jpg'
    encoded_data = wavTobase64(filename)
    post_to_Mobius(url, con_image, encoded_data)
    
      

def take_picture():
    print(">> take_picture() is called")
    now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    filepath = '/home/pi/offline_acousticIoT/images/'
    cmd = "fswebcam -r 1280x720 --no-banner " + filepath + now + '.jpg'
    #cmd = 'raspistill -t 1500 -w 1280 -h 720 -o ' + filepath + now + '.jpg'
    #cmd = 'raspistill -t 1500 -w 320 -h 240 -o ' + filepath + now + '.jpg'
    filename = filepath + now + '.jpg'
    #print(filename)
    os.system(cmd)


def wavTobase64(filepath):
    #print(">> wavTobase64() is called")
    if filepath:
        f = open(filepath, "rb")
        enc = base64.b64encode(f.read())
        f.close()
        #print("file exists")
        return str(enc)[2:-1]


def get_Mobius():
    payload = {}
    response = requests.request("GET", url_Mobius, data = payload)
    print("response.text: ", response.text)
    
def post_to_Mobius(url, con, encoded_data):
    print(">> post_to_Mobius(",url,",",con,") is called")
    url = url_Mobius + '/Mobius/raspberryPi/'+ con
    payload = """{
        "m2m:cin":{
            "con":{
                "data": "%s"
             }
         }
    }"""%(encoded_data)
    #print("payload: ", payload)
    #response = requests.request("POST", url, headers=headers, data=str(payload))
    #print(response.text)
    requests.request("POST", url, headers=headers, data=str(payload))


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
        