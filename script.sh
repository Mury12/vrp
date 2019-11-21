#! /bin/bash
#CHRISTOFIDES
echo "Solving CMT50.5"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse CMT50.5 > results/CMT50.5.txt;    
    else
        python3 main.py $i CMT50.5 >> results/CMT50.5.txt;
    fi
done
echo "Solving CMT75.11"
echo cmt75.11
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse CMT75.11 > results/CMT75.11.txt;    
    else
        python3 main.py $i CMT75.11 >> results/CMT75.11.txt;
    fi
done
echo "Solving CMT100.8"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse CMT100.8 > results/CMT100.8.txt;    
    else
        python3 main.py $i CMT100.8 >> results/CMT100.8.txt;
    fi
done
echo "Solving CMT120.7"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse CMT120.7 > results/CMT120.7.txt;    
    else
        python3 main.py $i CMT120.7 >> results/CMT120.7.txt;
    fi
done

#GOLDEN ET. AL
echo "Solving GOLD253.7"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse GOLD253.27 > results/GOLD253.27.txt;   
    else
        python3 main.py $i GOLD253.27 >> results/GOLD253.27.txt;
    fi
done
echo "Solving GOLD300.28"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse GOLD300.28 > results/GOLD300.28.txt;  
    else
        python3 main.py $i GOLD300.28 >> results/GOLD300.28.txt;
    fi
done
echo "Solving GOLD421.41"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse GOLD421.41 > results/GOLD421.41.txt;   
    else
        python3 main.py $i GOLD421.41 >> results/GOLD421.41.txt;
    fi
done

#SET M TOTH
echo "Solving MN10110"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse MN10110 > results/MN10110.txt;
    else
        python3 main.py $i MN10110 >> results/MN10110.txt;
    fi
done
echo "Solving M15112"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse MN15112 > results/MN15112.txt;
    else
        python3 main.py $i MN15112 >> results/MN15112.txt;
    fi
done
echo "Solving MN20016"
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i parse MN20016 > results/MN20016.txt;    
    else
        python3 main.py $i MN20016 >> results/MN20016.txt;
    fi
done