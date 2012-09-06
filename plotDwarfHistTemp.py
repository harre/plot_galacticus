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
savepath = 'radialStudies/'
#inputfile = '/media/daten/transfer/galacticus.hdf5'
inputfile = 'inputtemp'

h5file = tables.openFile(inputfile,"r")

timeTable = getData.getTimestepTable(h5file)
print timeTable

# In order to plot the physical values we need h
h = 0.73

# Boxsize in Mpc, for easy centering
#boxSize = 32000/1000

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
maxCoord = np.zeros(3)

print 'Coordinates of the center of mass: ', comCoord[0], comCoord[1], comCoord[2]

maxCoord[0] = nodeData.positionX[0]
maxCoord[1] = nodeData.positionY[0]
maxCoord[2] = nodeData.positionZ[0]
for i in range(1,nHalos):
	if nodeData.nodeMass[i] > nodeData.nodeMass[i-1]:
	      maxCoord[0] = nodeData.positionX[i]
	      maxCoord[1] = nodeData.positionY[i]
	      maxCoord[2] = nodeData.positionZ[i]
maxCoord = maxCoord/timeTable[len(timeTable)-1,2]*h
print 'Coordinates of the maximal mass: ', maxCoord[0], maxCoord[1], maxCoord[2]

if math.sqrt((maxCoord[0]-comCoord[0])**2+(maxCoord[1]-comCoord[1])**2+(maxCoord[2]-comCoord[2])**2) < 5: 
	print 'Center of mass and coordinates of heaviest Halo are less than 5 MPc' 
if math.sqrt((maxCoord[0]-comCoord[0])**2+(maxCoord[1]-comCoord[1])**2+(maxCoord[2]-comCoord[2])**2) > 5: 
	print 'ATTENTION: Center of mass and coordinates of heaviest Halo are too far away' 
	print math.sqrt((maxCoord[0]-comCoord[0])**2+(maxCoord[1]-comCoord[1])**2+(maxCoord[2]-comCoord[2])**2)
	
#tStart = 0
tEnd = len(timeTable)
##for i in range(tStart,tEnd):
##for i in range(tstep,tstep+1):
#tstep = i
#print 'tStep', tstep 
## get the dataset for time = timeTable[tstep,1]
#nodeData = getData.getOutput(h5file,timeTable[tstep,1])

nHalos = len(nodeData.positionX)
# ATTENTION: Positions seem to be in Mpc/h
# ATTENTION: Also check for the masses
positionX = nodeData.positionX[0:nHalos]
positionY = nodeData.positionY[0:nHalos]
positionZ = nodeData.positionZ[0:nHalos]
nodeMass  = nodeData.nodeMass[0:nHalos]
#gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.diskStellarMass[0:nHalos]+1E-16)
#gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.diskStellarMass[0:nHalos]+nodeData.spheroidStellarMass[0:nHalos]+1E-16)
gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.nodeMass[0:nHalos])
#siblingNode = nodeData.siblingNode[0:nHalos]
#starFormation = nodeData.diskStarFormationRate[0:nHalos]+nodeData.spheroidStarFormationRate[0:nHalos]
#diskAngularMomentum = nodeData.diskAngularMomentum[0:nHalos]
#print 'siblingNode', siblingNode	  

# Plot the inner 2 Mpc and color code them
plimit=5.0	       # allowed distance from the center in Mpc
title = 'Halo Positions'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Select points according to position
pmask=np.zeros(nHalos)
pmask=pmask.astype(bool)
# shift the halos to be centered around the center of mass
#for i in range(nHalos):
	#positionX[i] = positionX[i]-maxCoord[0]
	#positionY[i] = positionY[i]-maxCoord[1]
	#positionZ[i] = positionZ[i]-maxCoord[2]
maxx = max(positionX)
maxy = max(positionY)
maxz = max(positionZ)
for i in range(nHalos):
	positionX[i] = positionX[i]-maxx/2
	positionY[i] = positionY[i]-maxy/2
	positionZ[i] = positionZ[i]-maxz/2
#for i in range(nHalos):
	#mask[i] = False
	#pmask[i] = (np.abs(positionX[i]) < plimit and
		    #np.abs(positionY[i]) < plimit and
		    #np.abs(positionZ[i]) < plimit )
	  #mask[i] = True & pmask[i]	    
# Select points according to other criteria
mask=np.zeros(nHalos)
mask=mask.astype(bool)

print inputfile 
plimit1=0.5
mean1 = 0
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit1)
	mask[i] = True & pmask[i]
	#print mask
print 'Number of Objects in bin 1', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean1 = np.mean(gasComponent[mask])
  
plimit2=1
mean2 = 0
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit1 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit2)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 2', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean2 = np.mean(gasComponent[mask])

mean3 = 0 
plimit3=1.5
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit2 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit3)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 3', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean3 = np.mean(gasComponent[mask])

mean4 = 0
plimit4=2
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit3 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit4)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 4', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean4 = np.mean(gasComponent[mask])

mean5 = 0
plimit5=2.5
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit4 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit5)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 5', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean5 = np.mean(gasComponent[mask])

mean6 = 0 
plimit6=3
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit5 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit6)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 6', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean6 = np.mean(gasComponent[mask])

mean7 = 0
plimit7=4
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit6 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit7)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 7', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean7 = np.mean(gasComponent[mask])

mean8 = 0
plimit8=5
for i in range(nHalos):
	mask[i] = False
	pmask[i] = (plimit7 < math.sqrt(positionX[i]**2+positionY[i]**2+positionZ[i]**2) < plimit8)
	mask[i] = True & pmask[i]	    
print 'Number of Objects in bin 8', len(gasComponent[mask]) 
if len(gasComponent[mask] != 0): 	
	mean8 = np.mean(gasComponent[mask])

mean = [mean1, mean2, mean3, mean4, mean5, mean6, mean7, mean8]
plimit = [plimit1-(plimit2-plimit1)/2.0, plimit2-(plimit3-plimit2)/2.0, plimit3-(plimit4-plimit3)/2.0, plimit4-(plimit5-plimit4)/2.0, plimit5-(plimit6-plimit5)/2.0, plimit6-(plimit7-plimit6)/2.0, plimit7-(plimit8-plimit7)/2.0, plimit8-(plimit7-plimit7)/2.0]

title = savepath+'Gas Component, inputtemp'
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(plimit, mean, 'ro', c='#424242')
ax.axis([0,5.5,5E-3,5E-1])
ax.set_yscale('log')
ax.set_xlabel(r'Radius from BCG in MPc')
ax.set_ylabel(r'Mean Gas Component with respect to NodeMass in radial bins')
ax.set_title(title)
plt.savefig(title+'.png',dpi=savedpi,format=fileformat)

h5file.close()
