

for j in $(ls *.hdf5); do
  
#    echo "plotDwarfHist"
#    cp plotDwarfHistTemp.py plotDwarfHist.py 
#    sed "s/inputtemp/$j/g" -i plotDwarfHist.py	
#    python plotDwarfHist.py
#    
#    echo "plotRadialProfiles"
#    cp plotRadialProfilesTemp.py plotRadialProfiles.py 
#    sed "s/inputtemp/$j/g" -i plotRadialProfiles.py	
#    python plotRadialProfiles.py
#    
#    echo "plotRadialSFRProfiles"
#    cp plotRadialProfilesSFRTemp.py plotRadialProfilesSFR.py 
#    sed "s/inputtemp/$j/g" -i plotRadialProfilesSFR.py	
#    python plotRadialProfilesSFR.py
#   
#    echo "plotRadialMorphoProfiles"
#    cp plotRadialProfilesMorphoTemp.py plotRadialProfilesMorpho.py 
#    sed "s/inputtemp/$j/g" -i plotRadialProfilesMorpho.py	
#    python plotRadialProfilesMorpho.py
#   
#    echo "plotPositionsWithSFR"
#    cp plotPositionsWithSFRTemp.py  plotPositionsWithSFR.py
#    sed "s/inputtemp/$j/g" -i plotPositionsWithSFR.py	
#    python plotPositionsWithSFR.py
   
   echo "plotPositionsWithSFRFractional"
   cp plotPositionsWithSFRFracTemp.py  plotPositionsWithSFRFrac.py
   sed "s/inputtemp/$j/g" -i plotPositionsWithSFRFrac.py	
   python plotPositionsWithSFRFrac.py
   
#    echo "plotPositionsWIthMasses"
#    cp plotPositionsWIthMassesTemp.py  plotPositionsWIthMasses.py
#    sed "s/inputtemp/$j/g" -i plotPositionsWIthMasses.py	
#    python plotPositionsWIthMasses.py
#    
#    echo "plotHistograms"
#    cp plotHistogramsTemp.py  plotHistograms.py
#    sed "s/inputtemp/$j/g" -i plotHistograms.py	
#    python plotHistograms.py 0 1 
  
  
done   

