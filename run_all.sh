#!/bin/bash

# Shell script for obtaining all evaluation and exceptions files

for FILE in sick_test_evaluation
do
	for MOD in a2e i2c_a2e e_i2c e_i2c_split_adj split_verb split_adj a2e_i2c_split_adj
	do
		for LK in True False
		do
			python get_conf_mats.py mod_evaluations/[$MOD][$LK]$FILE.csv
		done
	done
done	
