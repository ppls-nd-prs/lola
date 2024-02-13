for MOD in i2c_a2e e_i2c e_i2c_split_adj split_verb split_adj a2e_i2c_split_adj none
do
	for LK in True False
	do
		python3 get_conf_mats.py mod_evaluations/[$MOD][$LK]fracas-full_evaluation.csv
	done
done
