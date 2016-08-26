#----definitions
year=2014
months=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
#months=('12')

sat=aqua
sensor=modis
res=10km
aeroLev=lev15


echo Settings Y $(tput setaf 3)$year$(tput sgr 0) S $(tput setaf 3)$sat$(tput sgr 0) Se $(tput setaf 3)$sensor$(tput sgr 0) R $(tput setaf 3)$res$(tput sgr 0) LA $(tput setaf 3)$aeroLev$(tput sgr 0)

#----new procedure to extract------------
#
echo $(tput setaf 3)'Beginning extraction procedure' $(tput sgr 0)

for month in ${months[@]}
do 

echo Extracting data from month $month
time /opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py $year $month $sat $sensor $res $aeroLev  
echo Extraction was finished from month $month

done

echo $(tput setaf 1)'Extraction finished'$(tput sgr 0)
#-----------------------------------------


#----colletc data ------------------------
#
echo $(tput setaf 3)'Collecting data ...'$(tput sgr 0)
outputPath=/outputData/$sensor/$res/$year

for i in $(seq 0 5)
do
scp aerosol@compute-0-$i:/state/partition1/outputData/*$res*$year*.p $HOME/aotData$outputPath
done

echo $(tput setaf 1)'Collecting procedures is done'$(tput sgr 0)
#----------------------------------------


#----Join satellite data
#
echo $(tput setaf 3)'Writing data ...'$(tput sgr 0)

for month in ${months[@]}
do
python joinSatData.py $year $month $sat $sensor $res
done

echo $(tput setaf 1)'Data written is done'$(tput sgr 0)
#-----------------------------------------


#----Make time list-----------------------
#
echo  $(tput setaf 3)'Making time list ...'$(tput sgr 0)

python makeTimeList.py $year $sat $res

echo $(tput setaf 1)'Time list is done'$(tput sgr 0)
#-----------------------------------------


#----Aeronet collecting data-----------------------
#
echo  $(tput setaf 3)'Collecting aeronet data ...'$(tput sgr 0)

python aeronetDataLev15.py $year $sat $res $aeroLev

echo $(tput setaf 1)'Collecting procedure is done'$(tput sgr 0)
#-----------------------------------------

echo Settings Y $(tput setaf 3)$year$(tput sgr 0) S $(tput setaf 3)$sat$(tput sgr 0) Se $(tput setaf 3)$sensor$(tput sgr 0) R $(tput setaf 3)$res$(tput sgr 0) LA $(tput setaf 3)$aeroLev$(tput sgr 0)




#---Extract station AOT fron satellite passage
#/opt/openmpi/bin/mpiexec -n 12 -machinefile machines python aeroPyAqua.py 2014 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 12 -machinefile machines python aeroPyAqua.py 2015 aqua modis 3km lev15 

#------
#time /opt/openmpi/bin/mpiexec -n 12 -machinefile $1 python aeroPyAqua.py $2 aqua modis 3km lev15  
#echo $1
#echo $2



#------
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 01 aqua modis 3km lev15  
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 02 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 03 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 04 aqua modis 3km lev15 

#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 05 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 06 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 07 aqua modis 3km lev15
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 08 aqua modis 3km lev15 

#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 09 aqua modis 3km lev15
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 10 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 11 aqua modis 3km lev15 
#/opt/openmpi/bin/mpiexec -n 31 -machinefile machines python aeroPyAquaExp.py 2015 12 aqua modis 3km lev15 







#echo $lev

#        ./control.sh $year $lev
#	./control2.sh $year $lev

 #       ./controlNppEdr.sh $year $lev
 #       ./controlNppEdr2.sh $year $lev

 #       ./makeTimeList.py $year aqua_nasa
 #       ./makeTimeList.py $year edrNppNasa

#        ./aeronetDataLev15.py $year aqua_nasa $lev
#        ./aeronetDataLev15.py $year edrNppNasa $lev
#done
