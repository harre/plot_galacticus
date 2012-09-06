reso=$1
hubble=$2 

for j in $(ls /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$1/$2/); do

  if [ $# -ne 2 ]; then
      echo " "
      echo ">> oOo.oOOoOops - argument needed: <res., i.e. r128 or r256> <hubble par., i.e. h70 or h100>"
      echo " "
      exit 1
  fi

  box=`grep BoxSize /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/*.tex | cut -c 22-28`
#   stringR=$box
#   boxi=${stringR:1} 
  
  
  if [ -d /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus/ ]; then 
  
  cp *.py /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus/
  cd /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus/ 
  sed "s/boxsizetemp/$box/g" -i plotPositions.py 		
  mkdir positionPlots
  python plotPositions.py 
  cp positionPlots/* /home/harre/dokumente/uni/phd/simulationen/doku/simulations_dok/$reso/$hubble/$j/
  fi 
  
  rev=708
  if [ -d /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ ]; then 
  
  cp *.py /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/
  cd /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ 
  sed "s/boxsizetemp/$box/g" -i plotPositions.py 		
  mkdir positionPlots
  python plotPositions.py 
  cp positionPlots/* /home/harre/dokumente/uni/phd/simulationen/doku/simulations_dok/$reso/$hubble/$j/
  fi 

  rev=709
  if [ -d /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ ]; then 
  
  cp *.py /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/
  cd /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ 
  mkdir positionPlots
  sed "s/boxsizetemp/$box/g" -i plotPositions.py 		
  python plotPositions.py 
  cp positionPlots/* /home/harre/dokumente/uni/phd/simulationen/doku/simulations_dok/$reso/$hubble/$j/
  fi 
 
  rev=771
  if [ -d /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ ]; then 
  
  cp *.py /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/
  cd /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ 
  mkdir positionPlots
  sed "s/boxsizetemp/$box/g" -i plotPositions.py 		
  python plotPositions.py 
  cp positionPlots/* /home/harre/dokumente/uni/phd/simulationen/doku/simulations_dok/$reso/$hubble/$j/
  fi 
 
  rev=836
  if [ -d /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ ]; then 
  
  cp *.py /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/
  cd /sshfsmount/astro-cluster/harre/simulations/gadget-structure-formation/$reso/$hubble/$j/output/galacticus_$rev/ 
  mkdir positionPlots
  sed "s/boxsizetemp/$box/g" -i plotPositions.py 		
  python plotPositions.py 
  cp positionPlots/* /home/harre/dokumente/uni/phd/simulationen/doku/simulations_dok/$reso/$hubble/$j/
  fi 
  
done   

