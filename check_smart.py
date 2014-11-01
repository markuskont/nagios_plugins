#!/usr/bin/env python

import sys, os, re

# Simply get all SMART data for device
def read_smart():
    cmd='sudo smartctl -a /dev/sda'
    
    return os.popen(cmd).read()

# check if device is HDD or SSD
def disk_type(argv):

    if re.search('Rotation Rate:\s*Solid\s*State\s*Device', argv, re.IGNORECASE):
        return "SSD"
    else:
        return "HDD"

def ssd_check_remaining_life(argv):

    # Media_Wearout_Indicator 0x0032   100   100   000    Old_age   Always       -       0

    life = re.search('Media_Wearout_Indicator\s0x\d+\s*(\d{1,3})', argv, re.IGNORECASE).group(1)

    # if critically low, create alert

    if life < 10:
        print("CRITICAL - %s percent lifetime left" % (life))
        sys.exit(2)
    elif life > 25:
        print("OK - %s percent lifetime left" % (life))
        sys.exit(0)
    else:
        print("WARNING - %s percent lifetime left" % (life))
        sys.exit(1)


def main():
    status=read_smart()

    if disk_type(status) == "SSD":
        ssd_check_remaining_life(status)

    elif disk_type(status) == "HDD":
        print "This is HDD"

    else:
        print "Not SSD nor HDD"

if __name__ == "__main__":
    main()
