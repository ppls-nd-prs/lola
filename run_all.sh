#!/bin/bash

for SET in sick_trial sick_train syllogisms
do
    for MOD in a2e i2c_a2e split none
    do
        for LK in True False
        do
            echo "Run with $SET - $MOD - $LK"
            python get_preds.py $SET $MOD $LK
        done
    done
done