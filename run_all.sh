#!/bin/bash

# Shell script for obtaining all evaluation and exceptions files

for SET in sick_trial sick_train sick_test syllogisms
do
    for MOD in a2e i2c_a2e split_verb split_adj none
    do
        for LK in True False
        do
            echo "Run with $SET - $MOD - $LK"
            python get_preds.py $SET $MOD $LK
        done
    done
done