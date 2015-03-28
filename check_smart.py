#!/usr/bin/env python

# THIS SCRIPT IS VERY BADLY WRITTEN

import sys, os, re, argparse

def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', help='Device node definition, e.g sda')
	args = parser.parse_args()

	return args

# Simply get all SMART data for device
def read_smart(node):

    if os.name == "posix":
        # sdX is hardcoded, but could be some other value than sdb
        # NOTE: read from function arcuments
        cmd='sudo smartctl -a /dev/' + node
    else:
        print "UNKNOWN - Not suported platform"
        sys.exit(3)
    
    return os.popen(cmd).read()

# check if device is HDD or SSD

def is_ssd(argv):
    if re.search('Rotation Rate:\s*Solid\s*State\s*Device', argv, re.IGNORECASE):
        return True
    else:
        return False

def extract_value_by_regex(pattern, data):
    return int(re.search(pattern, data, flags=re.MULTILINE|re.IGNORECASE).group(1))

def main():
    args = parse_arguments()
    dev_node = args.device

    if re.match('^sd\w$', dev_node):
        status=read_smart(dev_node)
    else:
        print "Invalid device node. Valid argument format is 'sd\w'"
        sys.exit(3)

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
