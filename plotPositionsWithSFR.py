#!/usr/bin/python

import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math 
import getData 
import os, sys, time, getopt, math, random
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp      
import matplotlib as mpl
import pyfits
from scipy import special
from matplotlib import rc
import os, sys, time, getopt, math, random
from matplotlib.ticker import MaxNLocator

savedpi = 250
fileformat = 'png'
savepath = 'positionPlots/'
#inputfile = '/media/daten/transfer/galacticus.hdf5'
inputfile = 'NGenIC_17794_2.hdf5'

h5file = tables.openFile(inputfile,"r")

timeTable = getData.getTimestepTable(h5file)
print timeTable

# In order to plot the physical values we need h
h = 0.72

# Boxsize in Mpc, for easy centering
boxSize = 32/1000

# Calculate the center of mass coordinates
# Get dataset at z=0
nodeData = getData.getOutput(h5file,timeTable[len(timeTable)-1,0])
#print 'Check time at center of mass calculation: ', timeTable[len(timeTable)-1,1]
nHalos = len(nodeData.positionX)
comCoord = np.zeros(3)
for i in range(nHalos):
	comCoord[0] += nodeData.positionX[i]
	comCoord[1] += nodeData.positionY[i]
	comCoord[2] += nodeData.positionZ[i]
comCoord = comCoord/nHalos/timeTable[len(timeTable)-1,2]*h
print 'Coordinates of the center of mass: ', comCoord[0], comCoord[1], comCoord[2]


maxCoord = np.zeros(3)


for i in range(nHalos):
        if nodeData.nodeMass[i] > nodeData.nodeMass[i-1]:
	      maxCoord[0] = nodeData.positionX[i-1]
	      maxCoord[1] = nodeData.positionY[i-1]
	      maxCoord[2] = nodeData.positionZ[i-1]
maxCoord = maxCoord/timeTable[len(timeTable)-1,2]*h
print 'Coordinates of the maximal mass: ', maxCoord[0], maxCoord[1], maxCoord[2]

tStart = 0
tEnd = len(timeTable)
for i in range(tStart,tEnd):
#for i in range(tstep,tstep+1):
	tstep = i
	# get the dataset for time = timeTable[tstep,1]
	nodeData = getData.getOutput(h5file,timeTable[tstep,1])

	nHalos = len(nodeData.positionX)
	# ATTENTION: Positions seem to be in Mpc/h
	# ATTENTION: Also check for the masses
	positionX = nodeData.positionX[0:nHalos]/timeTable[tstep,2]*h
	positionY = nodeData.positionY[0:nHalos]/timeTable[tstep,2]*h
	positionZ = nodeData.positionZ[0:nHalos]/timeTable[tstep,2]*h
	nodeMass  = nodeData.nodeMass[0:nHalos]
	gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.nodeMass[0:nHalos])
	starFormation = nodeData.diskStarFormationRate[0:nHalos]+nodeData.spheroidStarFormationRate[0:nHalos]

	# Plot the inner 2 Mpc and color code them
	plimit=5.0	       # allowed distance from the center in Mpc
	title = 'NGenIC_17794_2.hdf5 Halo Positions with absolute SFR'
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# Select points according to position
	pmask=np.zeros(nHalos)
	pmask=pmask.astype(bool)
	# shift the halos to be centered around the center of mass
#	for i in range(nHalos):
#		positionX[i] = positionX[i]-maxCoord[0]
#		positionY[i] = positionY[i]-maxCoord[1]
#		positionZ[i] = positionZ[i]-maxCoord[2]
        maxx = max(positionX)
        maxy = max(positionY)
        maxz = max(positionZ)
        for i in range(nHalos):
                positionX[i] = positionX[i]-maxx/2
                positionY[i] = positionY[i]-maxy/2
                positionZ[i] = positionZ[i]-maxz/2

	for i in range(nHalos):
		pmask[i] = (np.abs(positionX[i]) < plimit and
			    np.abs(positionY[i]) < plimit and
			    np.abs(positionZ[i]) < plimit )
	# Select points according to other criteria
	mask=np.zeros(nHalos)
	mask=mask.astype(bool)
	for i in range(nHalos):
		mask[i] = False
		if(starFormation[i]<1E8):
			mask[i] = True & pmask[i]
	# Attention: Scatter changes the alpha channel according to
	# the distance to the observing point, if you don't want this,
	# use plot3d instead
	nodeMassMean = math.log(np.mean(nodeData.nodeMass))
	print nodeMassMean
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='#848484',s=5,edgecolors='none')
       #ax.plot3D(positionX[mask], positionY[mask], positionZ[mask],'.',
       #	   c='k',ms=2.0)
	for i in range(nHalos):
		mask[i] = False
		if(1E8<starFormation[i]<1E9):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='#424242',s=10,edgecolors='none')
	for i in range(nHalos):
		mask[i] = False
		if(1E9<starFormation[i]<1E10):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		   ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			      c='#DF0174',s=25,edgecolors='none')
	for i in range(nHalos):
		mask[i] = False
		if(1E10<starFormation[i]<1E11):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='#9E0050',s=50,edgecolors='none')
	for i in range(nHalos):
		mask[i] = False
		if(1E11<starFormation[i]):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='#610B4B',s=150,edgecolors='none')		   
        # Set the axis labels
	ax.set_xlabel('Mpc (comoving)')
	ax.set_ylabel('Mpc')
	ax.set_zlabel('Mpc')
	ax.set_xlim3d(-plimit,plimit)	 
	ax.set_ylim3d(-plimit,plimit)
	ax.set_zlim3d(-plimit,plimit)
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' 5Mpc '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)


h5file.close()
