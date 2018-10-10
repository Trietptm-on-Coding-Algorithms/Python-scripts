#!/usr/bin/python
import sys 

buf = sys.argv[1]

if len(sys.argv[1]) <= 0:
	print "Usage : hextotext.py <HEX>"
	sys.exit(0)
print
for i in range (0,len(buf),2):
	sys.stdout.write(chr(ord(buf[i:i+2].decode('hex'))))

print