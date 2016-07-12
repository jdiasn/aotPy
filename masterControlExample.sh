year=('2014' '2015')
#year=('2014')

lev=lev15
#lev=lev20

for year in ${year[@]}
do

echo $lev

#        ./control.sh $year $lev
#	./control2.sh $year $lev

 #       ./controlNppEdr.sh $year $lev
 #       ./controlNppEdr2.sh $year $lev

 #       ./makeTimeList.py $year aqua_nasa
 #       ./makeTimeList.py $year edrNppNasa

        ./aeronetDataLev15.py $year aqua_nasa $lev
        ./aeronetDataLev15.py $year edrNppNasa $lev
done
