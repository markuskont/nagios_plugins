#!/usr/bin/env python

import sys, os, re

# Simply get all SMART data for device
def checksmart():
    cmd='sudo smartctl -a /dev/sda'
    status=os.system(cmd)
    return status

# check if device is HDD or SSD
def check_disk_type(argv):

    # DO SHIT HERE
    devicetype=re.search('Rotation Rate: ', argv)

    return devicetype

def main():
    status=checksmart()

    #print check_disk_type(status)

if __name__ == "__main__":
    main()
