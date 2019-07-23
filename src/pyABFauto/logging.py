import os
import datetime

PATH_HERE = os.path.dirname(os.path.abspath(__file__))
PATH_LOGFILE = os.path.join(PATH_HERE, "log.txt")

def timestamp():
    dt = datetime.datetime.now()
    stamp = str(dt)
    stamp = stamp.split(".")[0]
    return stamp

def log(message):
    message = f"{timestamp()} | {message}"
    print("", message)
    with open(PATH_LOGFILE, 'a') as f:
        f.write(message.strip()+"\n")

def warn(message):
    message = f"WARNING: {message}"
    print(message)
    log(message)