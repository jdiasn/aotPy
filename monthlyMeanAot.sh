echo 'Running extraction'

#year=2014


#----Extract process 
#/opt/openmpi/bin/mpiexec -n 12 -machinefile machines python aotModisAverage.py $year 


#----Extract process (chosing the machines)
#/opt/openmpi/bin/mpiexec -n 12 -machinefile machines1 python aotModisAverage.py 2014 
#/opt/openmpi/bin/mpiexec -n 12 -machinefile machines2 python aotModisAverage.py 2015 


#----Extrac process (chosing the month)
#months=('05' '06' '07' '08')
#for i in ${months[@]}
#do
#/opt/openmpi/bin/mpiexec -n 1 -machinefile machines python aotModisAverage.py 2014 $i &
#done

#----process to colect temp data
#----Join extracted data
#python joinData.py 2014 aqua modis 3
#python joinData.py 2015 aqua modis 3

echo 'Done' 
