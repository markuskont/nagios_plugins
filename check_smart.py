#!/usr/bin/env python

import sys, os, re

# Simply get all SMART data for device
def checksmart():
    cmd='sudo smartctl -a /dev/sda'
    
    return os.popen(cmd).read()

# check if device is HDD or SSD
def disk_type(argv):

    #devicetype=re.search('Rotation Rate:.+', argv)
    #SSD=re.compile('Rotation Rate:\s*solid\s*state\s*device', re.IGNORECASE)
    #SSD=re.search('Rotation Rate:.+')

    if re.search('Rotation Rate:\s*Solid\s*State\s*Device', argv):
        return "SSD"
    else:
        return "HDD"

def ssd_health_check(argv):

    print "this is SSD"

def hdd_health_check(argv):

    print "this is HDD"

def main():
    status=checksmart()

    if disk_type(status) == "SSD":
        ssd_health_check(status)

    elif disk_type(status) == "HDD":
        hdd_health_check(status)

    else:
        print "Not SSD nor HDD"

if __name__ == "__main__":
    main()
