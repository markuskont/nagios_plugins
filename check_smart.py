#!/usr/bin/env python

import sys, os

# Simply get all SMART data for device
def checksmart():
    cmd='sudo smartctl -a /dev/sda'
    status=os.system(cmd)
    return status

# check if device is HDD or SSD
def check_disk_type():
    print "asd"

def main():
    print checksmart()

if __name__ == "__main__":
    main()
