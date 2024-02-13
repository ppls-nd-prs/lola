for FILE in 01-fracas-quantifier 02-fracas-plural 03-fracas-anaphora 04-fracas-ellipsis 05-fracas-adjectives 06-fracas-comparatives 07-fracas-temporal 08-fracas-verbs 09-fracas-attitudes
do
	for MOD in a2e_i2c_split_adj
	do
		for LK in True
		do
			python3 get_conf_mats.py mod_evaluations/[$MOD][$LK]$FILE\_evaluation.csv
		done
	done
done
