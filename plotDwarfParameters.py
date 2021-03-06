#!/usr/bin/python

import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math 
import getData

savedpi = 250
fileformat = 'png'
savepath = './positionPlots/'
#inputfile = '/media/daten/transfer/galacticus.hdf5'
inputfile = './galacticus_stages_19.hdf5'

h5file = tables.openFile(inputfile,"r")

timeTable = getData.getTimestepTable(h5file)
print timeTable

# In order to plot the physical values we need h
h = 0.72

# Boxsize in Mpc, for easy centering
boxSize = 32000/1000

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
	#gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.diskStellarMass[0:nHalos]+1E-16)
	gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.diskStellarMass[0:nHalos]+nodeData.spheroidStellarMass[0:nHalos]+1E-16)
	#gasComponent = nodeData.diskGasMass[0:nHalos]/(nodeData.nodeMass[0:nHalos])
	siblingNode = nodeData.siblingNode[0:nHalos]
	starFormation = nodeData.diskStarFormationRate[0:nHalos]+nodeData.spheroidStarFormationRate[0:nHalos]
	diskAngularMomentum = nodeData.diskAngularMomentum[0:nHalos]
	#print 'siblingNode', siblingNode	  
	print 'gasComponent', gasComponent
	# Plot the whole n-body cube
	title = 'Halo Positions'
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(positionX,positionY,positionZ,alpha=0.3,s=0.5)
	ax.set_xlabel('Mpc (comoving)')
	ax.set_ylabel('Mpc')
	ax.set_zlabel('Mpc')
	ax.set_xlim(0,boxSize)
	ax.set_ylim(0,boxSize)
	ax.set_zlim(0,boxSize)
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)

	# Plot the inner 2 Mpc and color code them
	plimit=5.0	       # allowed distance from the center in Mpc
	title = 'Halo Positions'
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# Select points according to position
	pmask=np.zeros(nHalos)
	pmask=pmask.astype(bool)
	# shift the halos to be centered around the center of mass
	for i in range(nHalos):
		positionX[i] = positionX[i]-comCoord[0]
		positionY[i] = positionY[i]-comCoord[1]
		positionZ[i] = positionZ[i]-comCoord[2]

	for i in range(nHalos):
		pmask[i] = (np.abs(positionX[i]) < plimit and
			    np.abs(positionY[i]) < plimit and
			    np.abs(positionZ[i]) < plimit )
	# Select points according to other criteria
	mask=np.zeros(nHalos)
	mask=mask.astype(bool)
	#for i in range(nHalos):
		#mask[i] = False
		#if(nodeMass[i]<1E10):
			#mask[i] = True & pmask[i]
	## Attention: Scatter changes the alpha channel according to
	## the distance to the observing point, if you don't want this,
	## use plot3d instead
	#if len(positionX[mask])>0:
		#ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   #c='#848484',s=2.0,edgecolors='none')
       #ax.plot3D(positionX[mask], positionY[mask], positionZ[mask],'.',
       #	   c='k',ms=2.0)

	#for i in range(nHalos):
		#mask[i] = False
		#if(2E9<nodeMass[i]<2E10)  and siblingNode[i] == -1: 
			#mask[i] = True & pmask[i]
	#if len(positionX[mask])>0:
		#ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			  #c='#9E0050',s=gasComponent/1000,edgecolors='none')
	#for i in range(nHalos):
		#mask[i] = False
		#if(2E9<nodeMass[i]<2E10):
			#mask[i] = True & pmask[i]
	#if len(positionX[mask])>0:
		#ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			  #c='#424242',s=1,edgecolors='none')
	#for i in range(nHalos):
		#mask[i] = False
		#if(1E12<nodeMass[i]<1E13):
			#mask[i] = True & pmask[i]
	#if len(positionX[mask])>0:
		   #ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			      #c='#DF0174',s=40.0,edgecolors='none')
	#for i in range(nHalos):
		#mask[i] = False
		#if(1E13<nodeMass[i]<1E14):
			#mask[i] = True & pmask[i]
	#if len(positionX[mask])>0:
		#ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   #c='#9E0050',s=80.0,edgecolors='none')
	#for i in range(nHalos):
		#mask[i] = False
		#if(1E14<nodeMass[i]):
			#mask[i] = True & pmask[i]
	#if len(positionX[mask])>0:
		#ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   #c='#610B4B',s=150.0,edgecolors='none')		   
        # Set the axis labels
	#ax.set_xlabel('Mpc (comoving)')
	#ax.set_ylabel('Mpc')
	#ax.set_zlabel('Mpc')
	#ax.set_xlim3d(-plimit,plimit)	 
	#ax.set_ylim3d(-plimit,plimit)
	#ax.set_zlim3d(-plimit,plimit)
	#ax.set_title(title)
	#fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	#title = (savepath+title+' 5Mpc '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	#plt.savefig(title,dpi=savedpi,format=fileformat)
	## 10 MPc
	#ax.set_xlabel('Mpc (comoving)')
	#ax.set_ylabel('Mpc')
	#ax.set_zlabel('Mpc')
	#ax.set_xlim3d(-plimit*2,plimit*2)	 
	#ax.set_ylim3d(-plimit*2,plimit*2)
	#ax.set_zlim3d(-plimit*2,plimit*2)
	#ax.set_title(title)
	#fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	#title = (savepath+title+' 10Mpc '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	#plt.savefig(title,dpi=savedpi,format=fileformat)
	## 2.5 Mpc 
	#ax.set_xlabel('Mpc (comoving)')
	#ax.set_ylabel('Mpc')
	#ax.set_zlabel('Mpc')
	#ax.set_xlim3d(-plimit/2,plimit/2)	 
	#ax.set_ylim3d(-plimit/2,plimit/2)
	#ax.set_zlim3d(-plimit/2,plimit/2)
	#ax.set_title(title)
	#fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	#title = (savepath+title+' 2.5Mpc '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	#plt.savefig(title,dpi=savedpi,format=fileformat)
	
	# plot the star formation rate history versus time
	
	title = 'Gas Component'
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in range(nHalos):
	  	mask[i] = False
		if(nodeMass[i]<1E9):
			mask[i] = True & pmask[i]
			rad = (positionX**2+positionY**2+positionZ**2)
	if len(positionX[mask])>0:
		ax.plot(rad[mask],gasComponent[mask],'ro',c='#848484')	
	for i in range(nHalos):
	  	mask[i] = False
		if(1E9<nodeMass[i]<1E10):
			mask[i] = True & pmask[i]
			rad = (positionX**2+positionY**2+positionZ**2)
	if len(positionX[mask])>0:
		ax.plot(rad[mask],gasComponent[mask],'ro',c='#424242')
	for i in range(nHalos):
	  	mask[i] = False
		if(1E10<nodeMass[i]<1E11):
			mask[i] = True & pmask[i]
			rad = (positionX**2+positionY**2+positionZ**2)
	if len(positionX[mask])>0:
		ax.plot(rad[mask],gasComponent[mask],'ro',c='#DF0174')	
	for i in range(nHalos):
	  	mask[i] = False
		if(1E11<nodeMass[i]<1E12):
			mask[i] = True & pmask[i]
			rad = (positionX**2+positionY**2+positionZ**2)
	if len(positionX[mask])>0:
		ax.plot(rad[mask],gasComponent[mask],'ro',c='#9E0050')	
	for i in range(nHalos):
	  	mask[i] = False
		if(1E12<nodeMass[i]<1E13):
			mask[i] = True & pmask[i]
			rad = (positionX**2+positionY**2+positionZ**2)
	if len(positionX[mask])>0:
		ax.plot(rad[mask],gasComponent[mask],'ro', c='#610B4B')	
		ax.set_xlabel('Radius')
	ax.axis([0,25,1E-5,1E6])
	ax.set_yscale('log')	
	ax.set_ylabel(r'GasComponent')
	ax.set_title(title)
	plt.savefig(title,dpi=savedpi,format=fileformat)

h5file.close()
