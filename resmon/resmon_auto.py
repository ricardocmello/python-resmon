#!/usr/bin/env python

import sys
from datetime import datetime
import os
import signal
import subprocess
import time
import re

def main():
    if(len(sys.argv) != 2):
        print("Usage : {} file_name".format(sys.argv[0]))
        print("e.g.   {} test.csv".format(sys.argv[0]))
        sys.exit(-1)

    current_time = datetime.now().strftime("%Y%m%d_%I:%M%p")

    filename = current_time + "_" + sys.argv[1]

    print("Gather WiFi Metrics")
    command = 'ip link | grep wl | awk \'{printf \"%s\", $(2)}\''
    interface = str(subprocess.check_output(command,shell=True).decode('ascii'))
    interface = re.sub(r'[\W_]+', '', interface)
    print("WiFi interface used: {}".format(str(interface)))

    command = "resmon --delay 1 -f -o "+filename+" -n "+str(interface)+" --nic-outfile "+filename+"WiFi.csv"
    print(command)

    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    pro = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 

    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboar Interrupt")
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups

if __name__ == '__main__':
    main()