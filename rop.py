#!/usr/local/bin/python

import distorm3
from sys import argv, exit
import os

bits = distorm3.Decode64Bits

if (len(argv)) < 6:
	print("Usage : ropFunc.py <filepath> <outputFilepath> <fromOffset> <toOffset> <32/64 (default 64) >")
	exit()
print "Checked program is %s" % (os.path.basename(argv[1]))

if (int(argv[5],10) == 32):
	bits = distorm3.Decode32Bits

file = open(argv[1],"rb")
output = open(argv[2],"w")
buf = file.read()

decoded = distorm3.Decode(0,buf,distorm3.Decode64Bits)

if ("0x" in argv[3]):
	fromOffset = int(argv[3],16)
else:
	fromOffset = int(argv[3],10)
if ("0x" in argv[4]):
	toOffset = int(argv[4],16)
else:
	toOffset = int(argv[4],10)

start = 0
end = 0
i = 0
while (1):
	if (decoded[i][0] >= fromOffset):
		start = i-1
		break
	i = i + 1
i = 0
while (1):
	if (decoded[i][0] >= toOffset):
		end = i
		break
	i = i + 1
inst = i
print "Number of instructions in this section : ",i

rets = ["c3","cb","c2","ca"]

for i in xrange (start,end):
	if ("RET" in decoded[i][2]):
		for j in range (i-6,i+1):
			output.write ("%s |" % (str(decoded[j][2]).ljust(30)))
			output.write ("%s\n" % (hex(long(decoded[j][0])).rjust(25))[:-1])
		output.write("\n \n")
