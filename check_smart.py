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

def extract_value_by_regex(pattern, data):
    return re.search(pattern, data, flags=re.MULTILINE|re.IGNORECASE).group(1)

def main():
    status=read_smart()

    life = extract_value_by_regex('Media_Wearout_Indicator\s0x\S*\s*(\d{1,3})', status)
    faulty_sectors = extract_value_by_regex('Reallocated_Sector_Ct.+(\d+)$', status)

    if is_ssd(status):
        if int(life) < 15:
            print("CRITICAL - SSD lifetime alert; %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(2)
        elif int(faulty_sectors) > 0:
            print("WARNING - reallocated sectors; %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(1)
        elif int(life) > 40:
            print("OK - %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(0)
        else:
            print("UNKNOWN - %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(3)
    else:
        print "Not SSD"

if __name__ == "__main__":
    main()
