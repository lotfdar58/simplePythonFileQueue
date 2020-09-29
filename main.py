import queue
from threading import Thread

import os
import time
import mylogging

max_queue_size = 1
max_retry = 2

source_file="Source/test.txt"

file_queue = queue.Queue(max_queue_size)
notify_queue = queue.Queue(max_queue_size)

# Check if file exists in Source
# Move file from Source to Desc
# Print file from Desc

def check_if_files_exist():
    while True:
        mylogging.info("check file.")
        file_to_monitor = file_queue.get(True)
        mylogging.info("Waiting for " + file_to_monitor)
        while not os.path.isfile(file_to_monitor):
            time.sleep(5)
        file_returned = file_to_monitor
        mylogging.info("Got " + file_returned)
        notify_queue.put(file_returned)


if __name__ == "__main__":
    t = Thread(target=check_if_files_exist, args=())
    t.setDaemon(True)
    t.start()
    retry = 0
    is_success = False
    sleep_between_retry = 5
    while  retry <= max_retry and not is_success:
        mylogging.info("Try again")
        if os.path.isfile(source_file):
            mylogging.info("file found!")
            file_queue.put(source_file)
            time.sleep(sleep_between_retry)
            is_success = True
        retry = retry + 1
    notify_file = notify_queue.get(True, 3)
    count = 0
    with open(notify_file) as fp:
        Lines = fp.readlines()
        for line in Lines:
            count += 1
            mylogging.info("Line{}: {}".format(count, line.strip()))
    mylogging.info("finish")

    exit(0)


