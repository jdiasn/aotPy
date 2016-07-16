year=$1
months=('01' '02' '03' '04')
lev=$2

for month in ${months[@]}
do
#	echo 2014$month $month
	./aeroPyAqua.py $year$month $month $lev
done

