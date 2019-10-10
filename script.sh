#! /bin/bash
for ((i=0; i<30; ++i))
do
    if [ "$i" = 0 ]
    then
        python3 main.py $i > results;    
    else
        python3 main.py $i >> results;
    fi
done
