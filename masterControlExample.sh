year=('2014' '2015')
#year=('2014')

lev=lev15
#lev=lev20

for year in ${year[@]}
do

echo $lev
#        ./aotPy/control.sh $year $lev
#	./aotPy/control2.sh $year $lev

 #       ./aotPy/controlNppEdr.sh $year $lev
 #       ./aotPy/controlNppEdr2.sh $year $lev

 #       ./aotPy/makeTimeList.py $year aqua_nasa
 #       ./aotPy/makeTimeList.py $year edrNppNasa

        ./aotPy/aeronetDataLev15.py $year aqua_nasa $lev
        ./aotPy/aeronetDataLev15.py $year edrNppNasa $lev
done
