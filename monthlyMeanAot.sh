echo 'Running extraction'

#year=2014


#----Extract process 

#/opt/openmpi/bin/mpiexec -n 12 -machinefile machines1 python aotModisAverage.py $year 
/opt/openmpi/bin/mpiexec -n 12 -machinefile machines python aotModisAverage.py 2014 
/opt/openmpi/bin/mpiexec -n 12 -machinefile machines python aotModisAverage.py 2015 

#----Join extracted data
python joinData.py 2014 aqua modis 3
python joinData.py 2015 aqua modis 3

echo 'Done' 
