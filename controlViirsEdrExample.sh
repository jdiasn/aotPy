year=$1
months=('01' '02' '03')
lev=$2

for month in ${months[@]}
do
#       echo 2014$month $month
        ./aeroPyVirrsEdr.py $year$month $month $lev
done
