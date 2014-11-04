#!/usr/bin/env python

import sys, os, re

# Simply get all SMART data for device
def read_smart():

    if os.name == "posix":
        # sdX is hardcoded, but could be some other value than sdb
        # NOTE: read from function arcuments
        cmd='sudo smartctl -a /dev/sdb'

    elif os.name == "nt":
        # Does not work
        cmd="& 'C:\Program Files (x86)\smartmontools\bin\smartctl.exe' -a sdb"

    else:
        print "UNKNOWN - Not suported platform"
        sys.exit(3)
    
    return os.popen(cmd).read()

# check if device is HDD or SSD

def is_ssd(argv):
    if re.search('Rotation Rate:\s*Solid\s*State\s*Device', argv, re.IGNORECASE):
        return True
    elif os.name == "posix" and is_rotational() == False:
        return True
    else:
        return False

def is_rotational():
    # sdX is hardcoded, but could be some other value than sdb
    # NOTE: read from function arcuments
    fi="/sys/block/sdb/queue/rotational"

    if os.path.isfile(fi):
        data=open(fi, 'r') 
        if data.read() == 1:
            return True
        elif data.read() == 0:
            return False
        else:
            print("UNKNOWN - Strange data in %s" % (fi) )
            sys.exit(3)
    else:
        print "UNKNOWN - Unable to identify if disk is rotational or not"
        sys.exit(3)


def extract_value_by_regex(pattern, data):
    return int(re.search(pattern, data, flags=re.MULTILINE|re.IGNORECASE).group(1))

def main():
    status=read_smart()

    if is_ssd(status):

        life = extract_value_by_regex('Media_Wearout_Indicator\s0x\S*\s*(\d{1,3})', status)
        faulty_sectors = extract_value_by_regex('Reallocated_Sector_Ct.+(\d+)$', status)

        if life < 15:
            print("CRITICAL - SSD lifetime alert; %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(2)
        elif faulty_sectors > 0:
            print("WARNING - reallocated sectors; %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(1)
        elif life > 40:
            print("OK - %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(0)
        else:
            print("UNKNOWN - %s percent lifetime left; %s reallocated sectors" % (life, faulty_sectors))
            sys.exit(3)
    else:
        print "UNKNOWN - Script only supports SSD checking"
        sys.exit(3)

if __name__ == "__main__":
    main()
