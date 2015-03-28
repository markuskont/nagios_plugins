#!/usr/bin/env python

# THIS SCRIPT IS VERY BADLY WRITTEN

import sys, os, re, argparse

def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', help='Device node definition, e.g sda')
	args = parser.parse_args()

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(3)

	return args

def node_present(node):


	if re.match('^sd\w$', node):
		block_device = '/sys/block/' + node
		if os.path.exists(block_device):
			return True
		else:
			print "UNKNOWN - Node defined by user but cannot find under /sys/block/"
			sys.exit(3)
	else:
		print "UNKNOWN - Invalid device node. Valid argument format is 'sd\w'"
		sys.exit(3)

def read_smart(node):

	if node_present(node):
		cmd = 'sudo smartctl -a /dev/' + node
		return os.popen(cmd).read()

def main():
	args = parse_arguments()
	dev_node = args.device

	smart_raw = read_smart(dev_node)
	
	print smart_raw

if __name__ == "__main__":
    main()
