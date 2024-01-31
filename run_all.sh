#!/bin/bash

# Shell script for obtaining all evaluation and exceptions files

for SET in 07-fracas-temporal 09-fracas-attitudes
do
    echo "Run with $SET"
    python get_preds.py $SET none False
done
