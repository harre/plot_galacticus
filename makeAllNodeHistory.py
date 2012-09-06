#!/usr/bin/python

import os
import sys

nodeArrayIndex = sys.argv[1]

command = 'python getNodeHistory.py '+nodeArrayIndex
print command
os.system(command)

tStart=0
tEnd=199
for tstep in range(tStart,tEnd):
	command = 'python plotNodeHistory.py '+nodeArrayIndex+' '+str(tStart)+' '+str(tstep)
	print command
	os.system(command)

print 'finished with all the plots'
