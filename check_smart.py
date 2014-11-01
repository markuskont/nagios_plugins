#!/usr/bin/env python

import sys, os

def checksmart():
    cmd='sudo smartctl -a /dev/sda'
    status=os.system(cmd)
    return status

def main():
    print checksmart()

if __name__ == "__main__":
    main()
