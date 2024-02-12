for FILE in mod_evaluations/[none][True]fracas-full_evaluation.csv mod_evaluations/[split_adj][True]fracas-full_evaluation.csv evaluations/fracas-full_evaluation.csv
do
	python3 get_conf_mats.py $FILE
done
