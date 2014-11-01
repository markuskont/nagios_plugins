#!/usr/bin/env python

import sys, os, re

# Simply get all SMART data for device
def read_smart():
    cmd='sudo smartctl -a /dev/sda'
    
    return os.popen(cmd).read()

# check if device is HDD or SSD

def is_ssd(argv):
    if re.search('Rotation Rate:\s*Solid\s*State\s*Device', argv, re.IGNORECASE):
        return True
    else:
        return False

def check_health(argv):

    ssd=is_ssd(argv)

    life = re.search('Media_Wearout_Indicator\s0x\S*\s*(\d{1,3})', argv, flags=re.MULTILINE|re.IGNORECASE).group(1)
    faulty_sectors = re.search('Reallocated_Sector_Ct.+(\d+)$', argv, flags=re.MULTILINE|re.IGNORECASE).group(1)
    #faulty_sectors = 0

    if ssd == True:
        if int(life) < 15:
            print("CRITICAL - SSD lifetime alert; %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(2)
        elif int(faulty_sectors) > 0:
            print("WARNING - reallocated sectors; %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(1)
        elif int(life) > 30:
            print("OK - %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(0)
        else:
            print("WARNING - %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(1)
    else:
        print "Not SSD"


def main():
    status=read_smart()

    check_health(status)

if __name__ == "__main__":
    main()
