import sys
import os
if __name__ == '__main__':
    try:
        while 1:
            cmd = 'raspistill -w 1280 -h 720'
            os.system(cmd)
            
    except KeyboardInterrupt:
        print("Interrupted!!")
        sys.exit(0)
        